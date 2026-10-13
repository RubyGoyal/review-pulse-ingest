# Doc entry: W41 (as appended to the Google Doc)

Appended by the `append_to_doc` MCP tool after approval to **Weekly Product Pulse Log: ChatGPT Android (India)**.
It has the six required fields (`date`, `top_themes`, `weekly_pulse`, `identified_fee_issue`, `explanation_bullets`, `source_links`) as readable text, and the same fields again as one JSON line (`payload_json`) so the log can be parsed by a machine.

```text
────────────────────────────────────────
WEEKLY ENTRY · 2026-W41 · week ending 11 Oct 2026 · logged 14 Oct 2026
────────────────────────────────────────
date: 2026-10-14
top_themes: QUALITY, LIMITS, BUGS
identified_fee_issue: F_ACTIVATION: Charged but plan not activated (80 reviews in 10 weeks; stable)

weekly_pulse:
ChatGPT Android (India): Weekly Product Pulse
Week ending 11 Oct 2026 · 1197 Google Play reviews, 3 Aug 2026 – 11 Oct 2026

Top themes
1. Answer quality & reliability: 24% of reviews, 58% rated 1–2★. Wrong answers and repeated mistakes.
2. Usage limits & paywall: 19% of reviews, 48% rated 1–2★. Daily limits reached early, features locked.
3. App bugs & performance: 19% of reviews, 49% rated 1–2★. Glitches, voice not working, duplicated messages.

What users say
- "It provides wrong answers many of the times and frustrates." (2★, 7 Oct 2026)
- "I keep getting daily limit exhaust messages even when I'm not using image generation" (1★, 11 Oct 2026)
- "Now its copying my images and messages 5 times" (1★, 9 Oct 2026)

Key observation
Reports of being charged without plan activation are stable at 8 a week. Users describe ₹399 payments debited while accounts stay on Free, and say support is unreachable.

Action ideas
1. Fix paid-plan activation: Reconcile Google Play payments automatically and add a clear support route.
   Metric: Go purchases active in-app within 10 min ÷ Go purchases confirmed by Google Play
2. Reduce wrong answers: Review repeated-mistake reports and add in-chat feedback prompts.
   Metric: answer-quality 1–2★ reviews ÷ all reviews
3. Clarify usage limits: Show remaining quota before a limit message appears.
   Metric: limit-related 1–2★ reviews ÷ all reviews

explanation_bullets:
• What users are charged. Reviews from 3 Aug to 11 Oct 2026 describe ₹399 charges for ChatGPT Go bought in the Android app. These in-app plans are billed by Google Play and linked to both the Google Play account that paid and the ChatGPT account signed in at purchase.
• Why the app can still show Free. The plan only appears on the ChatGPT account used at purchase, and the Google Play email can differ from the ChatGPT email. Signing out and back in with the original ChatGPT account is how to access an existing subscription.
• Why ₹399 can be debited and later credited back. Google Play grants a purchase only once the payment completes. If a completed purchase is not confirmed by the app within 3 days, Google Play automatically refunds it and removes access.
• Check before paying again. The payment status is shown in the Play Store under Payments & subscriptions → Budget & history. Subscriptions cannot be moved between ChatGPT accounts, and buying again from another account can create a duplicate charge.
• Who resolves access. Google Play processes the payment; the app developer (OpenAI) is responsible for delivering a purchase that was paid for but not received in the app.
• Refunds. If the charge went through but the plan does not appear on the original ChatGPT account, a refund can be requested through Google Play or by contacting OpenAI.

source_links:
- https://help.openai.com/en/articles/20001056-why-am-i-seeing-a-message-that-my-subscription-is-associated-with-another-account
- https://support.google.com/googleplay/answer/1050566?hl=en
- https://developer.android.com/google/play/billing/integrate
Last checked: 13 Oct 2026

payload_json:
{"date":"2026-10-14","week":"2026-W41 (5 Oct 2026 – 11 Oct 2026)","top_themes":["QUALITY","LIMITS","BUGS"],"weekly_pulse":"# ChatGPT Android (India): Weekly Product Pulse\n**Week ending 11 Oct 2026** · 1197 Google Play reviews, 3 Aug 2026 – 11 Oct 2026\n\n## Top themes\n1. **Answer quality & reliability:** 24% of reviews, 58% rated 1–2★. Wrong answers and repeated mistakes.\n2. **Usage limits & paywall:** 19% of reviews, 48% rated 1–2★. Daily limits reached early, features locked.\n3. **App bugs & performance:** 19% of reviews, 49% rated 1–2★. Glitches, voice not working, duplicated messages.\n\n## What users say\n- \"It provides wrong answers many of the times and frustrates.\" (2★, 7 Oct 2026)\n- \"I keep getting daily limit exhaust messages even when I'm not using image generation\" (1★, 11 Oct 2026)\n- \"Now its copying my images and messages 5 times\" (1★, 9 Oct 2026)\n\n## Key observation\nReports of being charged without plan activation are stable at 8 a week. Users describe ₹399 payments debited while accounts stay on Free, and say support is unreachable.\n\n## Action ideas\n1. **Fix paid-plan activation:** Reconcile Google Play payments automatically and add a clear support route.\n   *Metric:* Go purchases active in-app within 10 min ÷ Go purchases confirmed by Google Play\n2. **Reduce wrong answers:** Review repeated-mistake reports and add in-chat feedback prompts.\n   *Metric:* answer-quality 1–2★ reviews ÷ all reviews\n3. **Clarify usage limits:** Show remaining quota before a limit message appears.\n   *Metric:* limit-related 1–2★ reviews ÷ all reviews","identified_fee_issue":"F_ACTIVATION: Charged but plan not activated (80 reviews in 10 weeks; stable)","explanation_bullets":["What users are charged. Reviews from 3 Aug to 11 Oct 2026 describe ₹399 charges for ChatGPT Go bought in the Android app. These in-app plans are billed by Google Play and linked to both the Google Play account that paid and the ChatGPT account signed in at purchase.","Why the app can still show Free. The plan only appears on the ChatGPT account used at purchase, and the Google Play email can differ from the ChatGPT email. Signing out and back in with the original ChatGPT account is how to access an existing subscription.","Why ₹399 can be debited and later credited back. Google Play grants a purchase only once the payment completes. If a completed purchase is not confirmed by the app within 3 days, Google Play automatically refunds it and removes access.","Check before paying again. The payment status is shown in the Play Store under Payments & subscriptions → Budget & history. Subscriptions cannot be moved between ChatGPT accounts, and buying again from another account can create a duplicate charge.","Who resolves access. Google Play processes the payment; the app developer (OpenAI) is responsible for delivering a purchase that was paid for but not received in the app.","Refunds. If the charge went through but the plan does not appear on the original ChatGPT account, a refund can be requested through Google Play or by contacting OpenAI."],"source_links":["https://help.openai.com/en/articles/20001056-why-am-i-seeing-a-message-that-my-subscription-is-associated-with-another-account","https://support.google.com/googleplay/answer/1050566?hl=en","https://developer.android.com/google/play/billing/integrate"],"last_checked":"2026-10-13"}
```
