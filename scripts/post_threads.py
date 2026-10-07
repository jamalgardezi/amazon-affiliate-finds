"""Daily Threads publisher. No external Python dependencies."""
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

STATE = Path("automation/threads-state.json")
API = "https://graph.threads.net/v1.0"
EXPECTED_USERNAME = "gadgetguyfinds"

def caption(product):
    title = " ".join(product["title"].split())[:230]
    text = ("Pet find to explore: " + title + "\n\n"
            "Check the size, materials and suitability for your pet before buying. "
            "See current details on Amazon:\n" + product["url"] +
            "\n\n#ad As an Amazon Associate I earn from qualifying purchases.")
    if len(text) > 500:
        raise ValueError("Caption exceeds Threads limit")
    return text

def products():
    source = Path("products.js").read_text()
    match = re.fullmatch(r"\s*const PRODUCTS\s*=\s*(\[.*\])\s*;?\s*", source, re.S)
    if not match:
        raise ValueError("Unexpected catalog format")
    result = []
    for p in json.loads(match[1]):
        url = urllib.parse.urlparse(p.get("url", ""))
        if (p.get("category") == "Pet Products" and p.get("asin") and
            p.get("title") and url.scheme == "https" and
            url.hostname in ("www.amazon.com", "amazon.com") and
            urllib.parse.parse_qs(url.query).get("tag")):
            result.append(p)
    return result

def api(path, data=None):
    token = os.environ["THREADS_ACCESS_TOKEN"]
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    req = urllib.request.Request(API + path, data=body,
                                 headers={"Authorization": "Bearer " + token})
    # Do not retry writes: a lost response may still mean the post was published.
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except Exception:
        raise RuntimeError("Threads request failed. Check account authorization and inspect Threads before retrying.") from None

def save(state, message):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2) + "\n")
    for command in [
        ["git", "config", "user.name", "github-actions[bot]"],
        ["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"],
        ["git", "add", str(STATE)],
        ["git", "commit", "-m", message],
        ["git", "push", "origin", "HEAD:main"],
    ]:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

def main():
    state = json.loads(STATE.read_text())
    if state.get("pending"):
        raise RuntimeError("Unresolved posting attempt. Inspect Threads and reconcile pending state before continuing.")
    today = dt.datetime.now(ZoneInfo("Asia/Dubai")).date().isoformat()
    if state.get("last_date") == today:
        print("Already posted today.")
        return
    used = {entry["asin"] for entry in state["posted"]}
    product = next((p for p in products() if p["asin"] not in used), None)
    if product is None:
        print("No unposted pet products remain. Add new catalog items.")
        return
    text = caption(product)
    live = (os.getenv("THREADS_ENABLED") == "true" and
            os.getenv("LIVE_REQUESTED") == "true")
    if not live:
        print("PREVIEW ONLY — nothing published.\n\n" + text)
        return
    if not os.getenv("THREADS_ACCESS_TOKEN"):
        raise RuntimeError("Add THREADS_ACCESS_TOKEN in GitHub Actions secrets.")
    identity = api("/me?fields=id,username")
    if identity.get("username", "").lower() != EXPECTED_USERNAME:
        raise RuntimeError("Token belongs to a different Threads account.")
    user_id = str(identity["id"])
    if not user_id.isdigit():
        raise RuntimeError("Invalid Threads account ID")
    state["pending"] = {"asin": product["asin"], "date": today, "text": text}
    # Persist intent BEFORE any publishing request. On uncertain outcome, stop.
    save(state, "Reserve daily Threads post")
    container = api("/" + user_id + "/threads", {"media_type": "TEXT", "text": text})
    state["pending"]["container_id"] = container["id"]
    save(state, "Record Threads container")
    published = api("/" + user_id + "/threads_publish", {"creation_id": container["id"]})
    state["posted"].append({"asin": product["asin"], "date": today, "post_id": published["id"]})
    state["last_date"] = today
    state["pending"] = None
    save(state, "Record published Threads product")
    print("Published Threads post ID: " + str(published["id"]))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Avoid raw network exceptions that could contain sensitive credentials.
        print("Posting stopped: " + (str(exc) if isinstance(exc, (RuntimeError, ValueError)) else type(exc).__name__), file=sys.stderr)
        sys.exit(1)
