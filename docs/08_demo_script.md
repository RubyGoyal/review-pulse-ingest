# Demo script: Review Pulse (about 2:45)

**Before recording, open these tabs:**
1. n8n: **0 Orchestrator** canvas
2. n8n: **5c Approve & publish** canvas
3. Google Sheet `Review_Pulse_DB`, on the **runs** tab
4. Gmail, with the approval email for a draft-ready week open, plus the **Drafts** folder
5. Google Doc **Weekly Product Pulse Log**
6. GitHub **Actions** page

To demo approval live, prepare a week first: run GitHub ingest for it, then run the orchestrator with *Week override* set to that week, so the approval email is waiting.

---

### 0:00–0:20 | The problem
> "ChatGPT's Android app gets thousands of Play Store reviews a week in India. Product teams need a short weekly signal, and support needs one clear answer for the most common charge confusion. I built an agent that produces both every Monday, and nothing is published until a human approves it."

### 0:20–0:45 | Data in (GitHub tab, then Sheet `ingest_log`)
> "At 7 AM on Monday, a GitHub Action collects last week's India reviews. It keeps a balanced sample of 125 reviews, 25 per star rating, plus every low-star billing review. The rows go into a Google Sheet, and the log marks the week as done."

### 0:45–1:25 | The agent (Orchestrator canvas)
> "At 8 AM the n8n orchestrator sees that the week is done and runs three steps.
> First, Analyse: Claude Haiku tags each review with one theme from a fixed codebook. Code, not the AI, computes 10-week shares, ratings and the fee trend.
> Second, Draft: Claude Sonnet writes the pulse. A validator then checks it's under 250 words, that every quote appears word for word in a real review, and that every number comes from the computed stats. If anything fails, it rewrites once.
> It also re-checks the official help pages behind the fee explainer every week."

### 1:25–2:00 | Approval gate (Gmail approval email, then 5c canvas)
> "Then it emails me for approval: the pulse, the explainer, the validation results and the source checks. The workflow is paused here, and nothing has been written anywhere yet."
>
> *Click **Approve & log**.*
>
> "Approving starts a Claude agent with an MCP client. It calls two MCP tools on my n8n MCP server: `append_to_doc` and `create_email_draft`. It passes only the week ID. The content comes from the approved record, so the agent can't change the text."

### 2:00–2:30 | Output (Doc, Gmail Drafts, Sheet `runs`)
> "Here's the entry in the Google Doc, with date, top themes, pulse, fee issue, explanation bullets and source links. Here's the Gmail draft, 'Weekly Product Pulse + Customer Clarification', which is never sent automatically. And in the Sheet, the week is marked published with the Doc link and the draft ID, so there's a full audit trail."

### 2:30–2:45 | Insight + close
> "This week's fee issue is 'charged ₹399 but still on Free'. That's 80 reviews in 10 weeks, and it's stable, not a spike. The explainer tells users why it happens and what to check before paying again. If anything fails along the way, I get one alert email. My only job each Monday is the approval click."
