# review-pulse-ingest

Weekly collector for the **Review Pulse** agent (NextLeap project). Every Monday at 07:00 IST
it pulls the previous week's Google Play reviews for ChatGPT (India store), samples them,
and appends new rows to the `reviews` tab of the Review Pulse DB Google Sheet. n8n then
picks up from the `ingest_log` tab.

## How it fits

```
GitHub Action (Mon 07:00 IST) ──► Google Sheet: reviews + ingest_log (status=done)
                                          │
n8n Orchestrator (Mon 08:00, hourly to 12:00) waits for done ──► Analyse ► Draft ► Approve ► Doc + Gmail draft
```

## Sampling (same as the Colab v3 notebook)
- Week = Monday–Sunday (ISO week), reviews with 4+ words, duplicates by text removed.
- **Base sample:** per star rating, 12 most-upvoted + 13 random (seeded by week ID) = up to 125 a week.
  Theme shares are calculated on this.
- **Fee boost:** every other 1–3★ review mentioning billing terms. Used only for fee-issue counts.
- Only `review_id`s not already in the Sheet are added, so re-runs never duplicate rows.

## Secrets (Settings → Secrets and variables → Actions)
| Name | Value |
|---|---|
| `GOOGLE_SA_JSON` | Full contents of the service-account JSON key |
| `SHEET_ID` | ID of the Review Pulse DB sheet |

The Sheet must be shared with the service account's email as **Editor**.

## Running by hand (Actions → Weekly review ingest → Run workflow)
- `dry_run` (default **on** for manual runs): fetch and count only, nothing written.
- `week_id`: e.g. `2026-W42`. Blank means the last full week.
- `force`: re-ingest a week already marked done.

Scheduled runs ignore these inputs: they always do a real run for the last full week.

## Statuses written to `ingest_log`
`running` → `done` | `low_volume` (base sample < `min_reviews_per_week`) | `failed` (error column has details).
n8n only continues on `done`; anything else triggers an alert email.
