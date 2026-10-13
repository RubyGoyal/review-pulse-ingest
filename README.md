# Review Pulse: weekly product pulse + fee explainer for ChatGPT Android (India)

Review Pulse is an AI workflow that runs every Monday:
1. It reads last week's Google Play reviews for ChatGPT (India store).
2. It finds the top themes and the most common fee/charge confusion.
3. It writes a short **weekly product pulse** and a **neutral fee explainer** with official sources.
4. **Only after a human approves**, it uses MCP tools to append the entry to a Google Doc and create a Gmail draft. Nothing is ever sent automatically.

**Live prototype:** _link added after setup_  ·  **Code:** this repo

**Fee issue identified:** **F_ACTIVATION, "Charged ₹399 for ChatGPT Go, but the app still shows Free"**. See [Which fee issue and why](#which-fee-issue-and-why).

---

## Deliverables

| File | What it is |
|---|---|
| [`docs/01_review_analysis.md`](docs/01_review_analysis.md) | Step 1: themes (max 5), top 3, 3 verbatim quotes, the recurring fee confusion |
| [`docs/02_weekly_pulse_W41.md`](docs/02_weekly_pulse_W41.md) | Step 2: weekly product pulse (226 words, limit 250): themes, quotes, key observation, 3 action ideas |
| [`docs/03_fee_explainer.md`](docs/03_fee_explainer.md) | Step 3: fee explainer (6 bullets, neutral, 3 official links, "Last checked") |
| [`docs/04_doc_entry_W41.md`](docs/04_doc_entry_W41.md) | Doc snippet: the exact entry appended to the Google Doc by the `append_to_doc` MCP tool |
| [`docs/05_email_draft_W41.html`](docs/05_email_draft_W41.html) | Email draft: "Weekly Product Pulse + Customer Clarification — 11 Oct 2026" (pulse + fee snippet), created as a Gmail **draft** |
| [`docs/06_reviews_sample.csv`](docs/06_reviews_sample.csv) | CSV sample: 25 reviews across all 10 weeks and all star ratings, including the reviews quoted in the pulse |
| [`docs/07_source_list.md`](docs/07_source_list.md) | Source list: 6 URLs (3 used in the explainer, 2 background, 1 data source) |
| [`docs/08_demo_script.md`](docs/08_demo_script.md) | Demo walkthrough (under 3 minutes) |
| [`n8n_workflows/`](n8n_workflows) | The 8 n8n workflows (import-ready JSON), including **6 Live page**, the public read-only prototype page |
| [`scripts/ingest.py`](scripts/ingest.py) + [`.github/workflows/`](.github/workflows) | The weekly review collector (Python + GitHub Actions). Details: [`docs/collector.md`](docs/collector.md) |

---

## How it works

```
Mon 07:00 IST  GitHub Actions ── ingest.py ──► Google Sheet "Review_Pulse_DB"
                                              (reviews + ingest_log: week = done)
                                                        │
Mon 08:00–12:00 n8n  0 Orchestrator (hourly; waits for "done")
                       ├─► 3b Analyse ........ Claude Haiku tags themes and fee types; code computes 10-week stats
                       ├─► 4 Draft & validate . checks official pages; Claude Sonnet writes pulse;
                       │                        code validates (≤250 words, verbatim quotes, numbers from stats);
                       │                        one automatic rewrite if validation fails
                       └─► 5c Approve & publish
                              │  Gmail "send and wait": approval email to the reviewer   ◄── HUMAN APPROVAL GATE
                              ▼  (only if Approve)
                           AI agent (Claude) ── MCP client ──► 5b MCP server
                                                                 ├─ tool append_to_doc ──► 5a ──► Google Doc
                                                                 └─ tool create_email_draft ► 5a ──► Gmail DRAFT
                           5c re-reads the Sheet: status "published" only if both results exist

Any failure ──► Error alert workflow ──► one email to the reviewer
Public link ──► 6 Live page (webhook) ──► latest approved pulse + explainer + status of every week
```

**Data store:** one Google Sheet with tabs `config`, `reviews`, `ingest_log`, `themes`, `fee_types`, `runs` (one row per week with status, stats, pulse, validation report, approval, links), `explainers` and `sources`.

**Design rules:**
- **The AI writes words; code computes every number.** Theme shares, counts and trends come from code. The validator rejects any number in the pulse that isn't in the computed statistics.
- **Quotes are verbatim.** Each quote must be an exact substring of a stored review.
- **Explainer facts are re-checked weekly.** Each official page is fetched and checked for key facts. If a fact disappears, the approval email flags the explainer for review.
- **MCP tools are safe to repeat.** The agent only passes `run_id`. The content comes from the approved Sheet row, never from new AI text. A tool that has already run returns its earlier result instead of writing again.
- **Re-runs are safe.** A week that is processing, awaiting approval or published is skipped.

---

## Where the approval happens

1. Workflow **5c Approve & publish** sends an email to the reviewer (`approver_email` in the `config` tab) containing the full pulse, the explainer, the validation results and the source checks.
2. The email has **Approve & log** and **Reject** buttons. The workflow **waits up to 48 hours**.
3. **Nothing is written to the Doc or Gmail before Approve.**
   - **Reject:** the week is marked `rejected` and nothing is written.
   - **No answer in 48h:** the week is marked `expired` and nothing is written.
4. **On Approve**, the Claude agent calls the two MCP tools exposed by **5b MCP server**:
   - `append_to_doc` appends `{date, top_themes, weekly_pulse, identified_fee_issue, explanation_bullets, source_links}` to the Google Doc.
   - `create_email_draft` creates the Gmail draft "Weekly Product Pulse + Customer Clarification — [date]". The workflow has **no send step**. A person sends it.
5. 5c then re-reads the Sheet and records `published`, with the Doc link and the draft ID.

Each week's audit trail is in the `runs` tab: `approval_sent_at`, `approved_at`, `approver_comment`, `doc_url`, `gmail_draft_id`.

---

## How to run

### Weekly (automatic)
Nothing to do. GitHub collects reviews at 07:00 IST every Monday, and the orchestrator runs between 08:00 and 12:00. The reviewer gets the approval email at about 08:15.

### Manually (any week)
1. **Collect reviews:** GitHub → `review-pulse-ingest` → Actions → *Weekly review ingest* → **Run workflow**. Set `week_id` (e.g. `2026-W42`, or blank for last week) and untick `dry_run`.
2. **Run the pipeline:** n8n → *0 Orchestrator* → set *Week override* to the same week (or blank) → **Execute workflow** (Run manually).
3. **Approve:** use the email.

### Set up from scratch
1. **Google Sheet:** create `Review_Pulse_DB` with the tabs above. Share it with the service account as Editor.
2. **GitHub:** a copy of this repo. Add the secrets `GOOGLE_SA_JSON` (service-account key) and `SHEET_ID`.
3. **n8n:** create the credentials *Google Sheets account*, *Gmail account*, *Google Docs account* and *Anthropic account*.
4. **Import** each JSON in `n8n_workflows/` as its **own** workflow.
5. **Connect the workflows:**
   - in **5b**, point both tools at *5a Tool actions*;
   - paste 5b's MCP **Production URL** into the MCP Client node in **5c**;
   - in **0 Orchestrator**, point the three *Run* nodes at 3b, 4 and 5c.
6. **Settings → Error workflow → *Error alert*** on 0, 3b, 4, 5a and 5c.
7. **Publish** Error alert, 5a, 5b, 3b, 4 and 5c, then the Orchestrator last.
8. **Optional:** publish **6 Live page** and share the Webhook's Production URL as the public prototype link.

---

## Which fee issue and why

**F_ACTIVATION, charged but the plan is not activated.**

**What users experience:**
- Users buy ChatGPT Go (₹399) or Plus in the Android app through Google Play, and the money is debited.
- The ChatGPT account still shows **Free / Upgrade**.
- Some pay again (double charge), some see the money credited back days later, and many ask for refunds.

**Why this issue:**
- **Largest recurring charge confusion:** 80 reviews in 10 weeks, all 1–3★.
- **India-specific:** reviews mention ₹399, Go, UPI and bank debits.
- **A misunderstanding that facts can fix**, which suits an explainer. Price complaints, for comparison, are opinions.
- **Trend:** stable. 32 in the first five weeks and 48 in the second, but billing reviews grew too, so the share went from 6.6% to 6.4% of low-star billing reviews.

**What the explainer covers:**
- why the plan is tied to the ChatGPT account used at purchase;
- Google Play's rule that a purchase not confirmed within **3 days is refunded automatically**;
- where to check the payment (Budget & history);
- why paying again can create a duplicate charge;
- who resolves access and how to ask for a refund.

**Sources:** OpenAI Help Center and Google Play Help (the explainer also cites Android Developers). ₹399 is the amount users report in reviews and is labelled that way.

---

## Sampling and method
- **Week:** Monday–Sunday (ISO week, IST). Reviews with fewer than 4 words and duplicate texts are dropped.
- **Base sample:** for each star rating, the 12 most-upvoted and 13 random reviews (seeded by week), so **up to 125 per week**. Theme shares use this sample.
- **Billing boost:** every other 1–3★ review mentioning billing terms. Used **only** for the fee-issue count.
- **Analysis window:** rolling 10 weeks (about 1,200 base reviews), so weekly noise doesn't drive the conclusions.
- **Tagging:** Claude Haiku in batches against a fixed codebook. The pipeline needs ≥95% of reviews tagged before it continues. Agreement with a hand-labelled pass is 85.5%.

## Limitations
- **The sample over-weights low ratings by design** (equal reviews per star), so theme shares describe the sample, not the whole Play Store.
- **One AI coder.** The tags have only been checked against one human pass (85.5% agreement). A second human spot-check would strengthen them.
- **Busy weeks can have gaps in 5★ coverage.** The collector caps how many reviews it fetches per star, and a week where a cap is hit is logged as `partial coverage` in `ingest_log`.
- **`developer.android.com` can't be reached from n8n Cloud**, so that source is marked *unreachable*, not *verified*. It doesn't block the run, and the other two sources are verified every week.
- **Google OAuth app in Testing mode:** if it stays in Testing, the Google credentials expire after 7 days and must be reconnected. Publishing the OAuth app removes this.
- **Scale:** the system handles about 350 new reviews a week. For much larger volumes, the tagging step would move to the Message Batches API.
