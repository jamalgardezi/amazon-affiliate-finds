#!/usr/bin/env python3
"""Free, dependency-free daily affiliate draft generator.

Uses existing affiliate URLs; does not scrape Amazon, claim live prices,
call AI services, or publish to social platforms.
"""
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "automation" / "daily-posts.md"
SITE = "https://jamalgardezi.github.io/amazon-affiliate-finds/"
OFFERS = [
    ("Amazon Coupons", "https://amzn.to/4hxthjB", "Browse available Amazon coupons and check eligibility at checkout."),
    ("Amazon Daily Deals", "https://amzn.to/3Vr0BjO", "Explore Amazon's daily deals and verify current prices and availability."),
]
STYLES = [
    "Looking for useful Amazon finds? Explore our curated categories and check today's offers.",
    "Shopping for tech, home, beauty or pet products? Browse Gardezi Finds and compare options.",
    "Discover curated Amazon product collections, with quick access to coupons and daily deals.",
    "Planning an Amazon purchase? Explore product categories and review current offers before ordering.",
]
today = datetime.now(timezone.utc).date()
i = today.toordinal() % len(STYLES)
offer = OFFERS[today.toordinal() % len(OFFERS)]
post = f"{STYLES[i]}\n\n{offer[0]}: {offer[1]}\nExplore: {SITE}\n\n#AmazonFinds #AmazonDeals"
if len(post) > 280:
    raise ValueError(f"X draft exceeds 280 characters: {len(post)}")
body = f"""# Gardezi Finds — Daily promotional drafts

Generated: {today.isoformat()} (UTC)

## X / Twitter draft

{post}

## Facebook / Threads draft

{STYLES[i]}

{offer[2]}

{offer[0]}: {offer[1]}
Browse categories: {SITE}

*Affiliate disclosure: As an Amazon Associate, I earn from qualifying purchases.*

## Notes

These are drafts, not published posts. Prices, discounts, product availability and eligibility must be checked on Amazon. The bot uses only existing links and requires no AI or product-data API.
"""
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(body, encoding="utf-8")
print(f"Wrote {OUT.relative_to(ROOT)}; X draft length: {len(post)}")
