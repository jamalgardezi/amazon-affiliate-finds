# Free Gardezi Finds affiliate draft bot

This bot generates daily promotional drafts for X and Facebook/Threads using existing affiliate links. It never publishes posts, scrapes Amazon, or calls AI/paid APIs.

- Daily schedule: 07:20 UTC (11:20 UAE time), subject to GitHub Actions scheduling delays.
- Manual run: GitHub repository > Actions > Free Daily Affiliate Drafts > Run workflow.
- Output: [daily-posts.md](daily-posts.md).
- Existing coupon link: https://amzn.to/4hxthjB
- Existing daily deals link: https://amzn.to/3Vr0BjO

The workflow commits drafts back to the main branch using GitHub Actions' built-in token. Repository settings must allow Actions to read/write contents. If GitHub Actions is disabled or the scheduled workflow is paused, drafts will not update. Existing Threads automation is unaffected.

The generated posts are drafts only. Review claims, current offers, affiliate disclosures and social-platform policies before publishing. GitHub Pages hosting and affiliate-site policy restrictions should be reviewed separately.
