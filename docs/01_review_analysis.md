# Step 1: Review analysis (ChatGPT Android, India store, W41)

**Data:** Google Play reviews from the India store for `com.openai.chatgpt`, covering 10 weeks (3 Aug – 11 Oct 2026).
- **Base sample (1,197 reviews):** up to 25 per star rating per week, made up of 12 most-upvoted and 13 random. All theme shares below come from this sample.
- **Billing boost (1,125 reviews):** every other 1–3★ review that mentions billing. These are used only to count the fee issue.

**Method:**
- Claude (Haiku) tags each review with exactly one theme from a fixed codebook (Sheet tab `themes`) and a fee type from a fixed list (tab `fee_types`).
- All counts, shares and trends are calculated in code, not by the AI.
- Tagging was checked against a hand-labelled pass: **85.5% agreement**.

---

## 1. Themes (5, plus an "unclear" bucket)

| # | Theme | Covers | Reviews | Share | Avg ★ | % 1–2★ |
|---|---|---|---|---|---|---|
| 1 | **Answer quality & reliability** | Wrong or outdated answers, ignored instructions, forgotten context, over-strict refusals, poor image edits | 289 | 24% | 2.3 | 58% |
| 2 | **Usage limits & paywall** | Message, image and attachment caps; reset times; upgrade prompts; ads; price | 232 | 19% | 2.7 | 48% |
| 3 | **App bugs & performance** | Crashes, lost messages, "message not sent", login, voice glitches, UI changes | 222 | 19% | 2.6 | 49% |
| 4 | Subscription & billing | Payments, plan activation, cancelling, refunds | 7 | <1% | 2.0 | 71% |
| 5 | Praise & feature requests | Positive use and requests without a complaint | 338 | 28% | 4.1 | 9% |
| – | *Unclear / off-topic* | Too vague to classify; not counted as a theme | 109 | 9% | 2.0 | 73% |

**Why billing looks small:** billing reviews are rare in the base sample, so the fee issue is measured on the billing boost set instead (section 4).

## 2. Top 3 themes

The top 3 are ranked by volume among the complaint themes:
1. **Answer quality & reliability**: 24% of reviews, 58% of them rated 1–2★.
2. **Usage limits & paywall**: 19%, 48% rated 1–2★.
3. **App bugs & performance**: 19%, 49% rated 1–2★.

## 3. Three user quotes (verbatim, one per top theme)

> **Quality:** "It provides wrong answers many of the times and frustrates." (2★, 7 Oct 2026)

> **Limits:** "I keep getting daily limit exhaust messages even when I'm not using image generation" (1★, 11 Oct 2026)

> **Bugs:** "Now its copying my images and messages 5 times" (1★, 9 Oct 2026)

Each quote is checked in code as an exact substring of a review stored in the Sheet.

## 4. Recurring fee/charge confusion: **F_ACTIVATION, "Charged but plan not activated"**

**What happens:**
- Users buy ChatGPT Go (₹399) or Plus in the Android app through Google Play.
- The money leaves their bank or UPI account, but the ChatGPT account still shows **Free / Upgrade**.
- Some pay a second time and end up double-charged. Some see the money credited back days later. Many ask for refunds.

**Evidence:**
- **80 reviews** in 10 weeks, all 1–3★.
- **Trend: stable.** 32 in the first 5 weeks, 48 in the last 5. Billing reviews overall grew too, so as a share of low-star billing reviews it went from 6.6% to 6.4%. That's stable, not a spike.
- **India-specific:** many reviews mention ₹399, "Go", UPI or a bank debit.

**Representative quote:**
> "I HAVE Purchased GO plan and paid rs.399/- but plan not activated still showing upgrade." (1★, 18 Sep 2026)

**Why this issue and not the others:**

| Candidate | Why not chosen |
|---|---|
| Paid plan still hits limits | It's about what the plan includes, not a charge, and is mostly global and priced in USD. |
| Price too high | It's a complaint, not a misunderstanding that an explainer can clear up. |
| Charged after cancelling / auto-renew | Real, but about a third of the size and less India-specific. |

**A note on the count:** the first manual pass found 43 cases. Claude's tagging finds 80, because it catches more ways of describing the same problem, for example "Play Store shows purchased, app shows upgrade" or "Restore purchase did nothing". The automated count is the one the weekly agent uses.
