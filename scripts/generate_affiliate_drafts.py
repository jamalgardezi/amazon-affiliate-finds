#!/usr/bin/env python3
"""Prepare affiliate drafts from the existing catalog, without paid APIs.

No scraping, AI calls, automatic publishing, or claims of live prices.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "products.js"
OUTPUT = ROOT / "automation" / "daily-posts.md"
STATE = ROOT / "automation" / "affiliate-draft-state.json"
SITE = "https://jamalgardezi.github.io/amazon-affiliate-finds/"
COUPONS = "https://amzn.to/4hxthjB"
DEALS = "https://amzn.to/3Vr0BjO"

def load_products():
    raw = CATALOG.read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"const\s+PRODUCTS\s*=\s*(\[.*\])\s*;?", raw, re.S)
    if not match:
        raise ValueError("Unexpected products.js format; refusing to alter product data")
    return json.loads(match.group(1))

def safe_title(title, limit=90):
    title = " ".join(str(title).split())
    return title if len(title) <= limit else title[:limit - 1].rsplit(" ", 1)[0] + "…"

def eligible(p):
    asin = str(p.get("asin") or "").strip().upper()
    url = str(p.get("url") or "").strip()
    title = str(p.get("title") or "").strip()
    return bool(re.fullmatch(r"[A-Z0-9]{10}", asin) and title and
                re.fullmatch(r"https://www\.amazon\.com/dp/[A-Z0-9]{10}\?tag=[A-Za-z0-9_-]+-20", url) and
                url.split("/dp/")[1][:10] == asin)

def main():
    products = {}
    for p in load_products():
        if eligible(p):
            products.setdefault(p["asin"].upper(), p)
    if not products:
        raise ValueError("No eligible products with valid existing affiliate links")

    prior = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    used = set(prior.get("used_asins", []))
    choices = sorted(products)
    remaining = [asin for asin in choices if asin not in used]
    if not remaining:
        used.clear()
        remaining = choices
    asin = remaining[0]
    p = products[asin]
    used.add(asin)

    title = safe_title(p["title"])
    category = str(p.get("category") or "Amazon Finds").strip()
    url = p["url"]
    today = datetime.now(timezone.utc).date().isoformat()
    xpost = f"🛍️ Amazon find: {title}\n\nCategory: {category[:35]}\nView product: {url}\n\n#AmazonFinds"
    if len(xpost) > 280:
        title = safe_title(p["title"], 65)
        xpost = f"Amazon find: {title}\n{url}\n#AmazonFinds"
    if len(xpost) > 280:
        raise ValueError("X draft exceeds 280 characters")

    fbpost = f"""Today's Amazon find: {p['title']}

Category: {category}
Explore the product and verify current details, availability and pricing on Amazon:
{url}

More curated finds: {SITE}

Affiliate disclosure: As an Amazon Associate, I earn from qualifying purchases."""
    body = f"""# Gardezi Finds — Daily promotional drafts

Generated: {today} (UTC)
Selected ASIN: {asin}
Source: Existing `products.js` catalog (no live Amazon checks)

## X / Twitter draft

{xpost}

## Facebook / Threads draft

{fbpost}

## Other links to share

- Amazon Coupons: {COUPONS}
- Amazon Daily Deals: {DEALS}
- Gardezi Finds: {SITE}

## Review before publishing

Drafts only. Nothing is posted automatically. Confirm the product remains available, the affiliate link works, and all current claims on Amazon. Avoid stating prices, ratings or discounts without live verification. Comply with each social platform's affiliate disclosure requirements.
"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(body, encoding="utf-8")
    STATE.write_text(json.dumps({"used_asins": sorted(used), "last_asin": asin, "last_date": today}, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared draft for {asin} ({category}); {len(used)}/{len(products)} unique products used; X length {len(xpost)}")

if __name__ == "__main__":
    main()
