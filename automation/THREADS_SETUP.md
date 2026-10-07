# Daily Threads product posts

Account: https://www.threads.com/@gadgetguyfinds

Runs daily around 20:15 Asia/Dubai (16:15 UTC). GitHub schedules can be delayed.
Starts with Pet Products from products.js, one previously unposted ASIN per day.
Uses existing affiliate URLs unchanged. Captions do not assert current prices,
availability, discounts or historical ratings. Preview is the default.
No external AI subscription is needed.

## Authorize your account

1. Follow Meta's Threads setup: https://developers.facebook.com/documentation/threads/get-started
   Create a Meta developer app with the Threads use case and authorize your own
   gadgetguyfinds account. Complete any account-role/tester or review requirements
   shown by Meta for your app's access mode.
2. Grant threads_basic and threads_content_publish. Obtain a long-lived Threads
   user access token through Meta's supported flow. Never paste it into chat,
   commit it, or put it in a public repository variable.
3. Open https://github.com/jamalgardezi/amazon-affiliate-finds/settings/secrets/actions
   and add repository secret THREADS_ACCESS_TOKEN.
4. In Actions, open Daily Threads product and run it with publish unchecked.
   Review the caption in the log.
5. At https://github.com/jamalgardezi/amazon-affiliate-finds/settings/variables/actions
   add THREADS_ENABLED with value true. The next scheduled run will publish.
   For an immediate live run, use Run workflow with publish checked.
   Live runs verify the token belongs to gadgetguyfinds.

## Maintenance

Set THREADS_ENABLED=false to pause. Keep GitHub workflow-failure notifications on.
The token needs renewal: Meta long-lived tokens normally last 60 days.
Refresh/replace the secret before expiration using Meta's documented flow:
https://developers.facebook.com/documentation/threads/get-started/long-lived-tokens
This workflow does not store or rotate tokens in git.

State is committed before posting. Any unresolved pending attempt stops subsequent
posts rather than risking duplicates. If a run fails, inspect the Threads account.
If the post exists, add its ASIN, date and post_id to posted and set last_date.
Then clear pending. If it definitely did not publish, clear pending to allow retry.
Do not clear pending without checking the account.

The workflow needs permission to push state commits to main. Branch protections
may require a different state-storage design; do not weaken them to run this.
Concurrent main updates can cause a safe stop. Public repository schedules can
be disabled by GitHub after 60 days without activity; check the Actions page if
posts stop. Once all pet ASINs are used, the workflow stops posting until new
products are added. Product availability is not independently verified.

## Local preview

Run python3 scripts/post_threads.py from the repository root.
Without both enable flags, no API requests or state changes occur.
