"""
Weekly Play Store review ingest for the Review Pulse agent.

Runs every Monday on GitHub Actions. Pulls last ISO week's (Mon–Sun) reviews for the
app in the `config` tab, builds the same sample as the Colab v3 notebook, appends only
NEW review_ids to the `reviews` tab, and records the run in `ingest_log`.
n8n starts the analysis only when ingest_log shows status = done for that week.

Env vars (GitHub Secrets):
  GOOGLE_SA_JSON  full JSON key of the Google service account
  SHEET_ID        Review Pulse DB spreadsheet ID
Optional (manual runs):
  WEEK_ID         e.g. 2026-W42 to (re)ingest a specific week; default = last full week
  FORCE           "true" to re-run a week already marked done
"""
import json, os, random, re, sys, time, traceback
from datetime import datetime, timedelta, timezone

import gspread
from google_play_scraper import Sort, reviews

IST = timezone(timedelta(hours=5, minutes=30))
# 5★ volume is ~3,300/day in India, and a Monday run must reach back ~8 days.
RAW_CAP_PER_STAR = {1: 10000, 2: 5000, 3: 6000, 4: 12000, 5: 40000}
PARTIAL = []  # star ratings that hit the cap before reaching the week start
FEE_PATTERN = re.compile(
    r"refund|\bcharg(ed|ing|es)\b|deduct|debit|auto.?renew|renewal|subscri|billing|\bbill(ed)?\b|"
    r"payment|\bpaid\b|\bpay(ing)?\b|₹|\brs\.?\s?\d|\binr\b|rupee|\bgst\b|\btax\b|\bupi\b|auto.?pay|"
    r"mandate|money back|chatgpt plus|gpt plus|plus plan|plus subscription|go plan|chatgpt go|gpt go|"
    r"\bpro plan\b|premium|membership|\bprice|pricing|expensive|\bcost|free trial|\btrial\b|invoice",
    re.I,
)
REVIEW_COLS = ["review_id", "review_date", "week_id", "week_start", "rating", "text", "thumbs_up",
               "app_version", "sample_reason", "fee_mention", "theme_code", "theme_source",
               "fee_type", "run_id", "ingested_at"]
LOG_COLS = ["run_id", "started_at", "finished_at", "status", "reviews_fetched", "reviews_new",
            "date_from", "date_to", "error"]


def now_iso():
    return datetime.now(IST).strftime("%Y-%m-%dT%H:%M:%S")


def target_week():
    """Return (week_id, monday, next_monday) for WEEK_ID or the last full ISO week in IST."""
    wid = os.environ.get("WEEK_ID", "").strip()
    if wid:
        y, w = wid.split("-W")
        monday = datetime.fromisocalendar(int(y), int(w), 1)
    else:
        today = datetime.now(IST).replace(tzinfo=None)
        monday = (today - timedelta(days=today.weekday() + 7)).replace(hour=0, minute=0, second=0, microsecond=0)
    iso = monday.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}", monday, monday + timedelta(days=7)


def read_config(sh):
    rows = sh.worksheet("config").get_all_values()[1:]
    return {r[0]: r[1] for r in rows if r and r[0]}


def pull_star(app_id, country, lang, star, start, cap):
    out, token = [], None
    while len(out) < cap:
        for attempt in range(4):
            try:
                batch, token = reviews(app_id, lang=lang, country=country, sort=Sort.NEWEST,
                                       count=200, filter_score_with=star, continuation_token=token)
                break
            except Exception as e:  # network hiccup: back off and retry
                print(f"{star}★ attempt {attempt + 1} failed: {e}")
                time.sleep(5 * (attempt + 1))
        else:
            raise RuntimeError(f"Play Store fetch failed 4 times for {star}★")
        if not batch:
            break
        out += batch
        if batch[-1]["at"] < start:
            break
        time.sleep(0.3)
    oldest = out[-1]["at"] if out else None
    if oldest and oldest >= start and len(out) >= cap:
        PARTIAL.append(f"{star}★ from {oldest:%Y-%m-%d %H:%M}")
    print(f"{star}★: {len(out)} raw, oldest {oldest or '-'}")
    return out


def build_sample(raw, start, end, per_cell, seed):
    seen_text, by_star = set(), {s: [] for s in range(1, 6)}
    for r in raw:
        text = (r.get("content") or "").strip()
        if not (start <= r["at"] < end) or len(text.split()) < 4 or text in seen_text:
            continue
        seen_text.add(text)
        by_star[r["score"]].append(r)
    rng = random.Random(seed)
    base, chosen = [], set()
    for star, rows in by_star.items():
        top_n = per_cell // 2
        top = sorted(rows, key=lambda r: r.get("thumbsUpCount") or 0, reverse=True)[:top_n]
        rest = [r for r in rows if r not in top]
        rnd = rng.sample(rest, min(per_cell - len(top), len(rest)))
        for r, why in [(r, "top_upvoted") for r in top] + [(r, "random") for r in rnd]:
            base.append((r, why)); chosen.add(r["reviewId"])
    boost = [(r, "fee_boost") for star in (1, 2, 3) for r in by_star[star]
             if r["reviewId"] not in chosen and FEE_PATTERN.search(r["content"])]
    total_in_window = sum(len(v) for v in by_star.values())
    return base, boost, total_in_window


def to_row(r, why, week_id, week_start, run_id, ts):
    text = r["content"].replace("\r", " ").strip()
    return {
        "review_id": r["reviewId"], "review_date": r["at"].strftime("%Y-%m-%dT%H:%M:%S"),
        "week_id": week_id, "week_start": week_start.strftime("%Y-%m-%d"), "rating": r["score"],
        "text": text, "thumbs_up": r.get("thumbsUpCount") or 0,
        "app_version": r.get("reviewCreatedVersion") or "", "sample_reason": why,
        "fee_mention": "TRUE" if FEE_PATTERN.search(text) else "FALSE",
        "theme_code": "", "theme_source": "", "fee_type": "", "run_id": run_id, "ingested_at": ts,
    }


def upsert_log(ws, row):
    ids = ws.col_values(1)
    values = [[row.get(c, "") for c in LOG_COLS]]
    if row["run_id"] in ids:
        ws.update(values, f"A{ids.index(row['run_id']) + 1}", value_input_option="RAW")
    else:
        ws.append_rows(values, value_input_option="RAW")


def main():
    gc = gspread.service_account_from_dict(json.loads(os.environ["GOOGLE_SA_JSON"]))
    sh = gc.open_by_key(os.environ["SHEET_ID"])
    cfg = read_config(sh)
    log_ws, rev_ws = sh.worksheet("ingest_log"), sh.worksheet("reviews")
    week_id, start, end = target_week()
    force = os.environ.get("FORCE", "").lower() == "true"
    dry_run = os.environ.get("DRY_RUN", "").lower() == "true"

    if dry_run:  # fetch + sample only; write nothing to the Sheet
        raw = []
        for star in range(1, 6):
            raw += pull_star(cfg["app_id"], cfg["country"], cfg["lang"], star, start, RAW_CAP_PER_STAR[star])
        base, boost, in_window = build_sample(raw, start, end, int(cfg["per_cell_cap"]), seed=week_id)
        print(f"DRY RUN {week_id}: {in_window} reviews in window, base {len(base)}, boost {len(boost)}. "
              f"Partial coverage: {', '.join(PARTIAL) or 'none'}. Nothing written.")
        sys.exit(0 if len(base) >= int(cfg["min_reviews_per_week"]) else 1)

    existing_log = {r[0]: r for r in log_ws.get_all_values()[1:] if r}
    if week_id in existing_log and existing_log[week_id][3] == "done" and not force:
        print(f"{week_id} already done. Set FORCE=true to re-run."); return

    log = {"run_id": week_id, "started_at": now_iso(), "status": "running",
           "date_from": start.strftime("%Y-%m-%d"), "date_to": (end - timedelta(days=1)).strftime("%Y-%m-%d")}
    upsert_log(log_ws, log)
    try:
        app_id, country, lang = cfg["app_id"], cfg["country"], cfg["lang"]
        per_cell, min_reviews = int(cfg["per_cell_cap"]), int(cfg["min_reviews_per_week"])
        raw = []
        for star in range(1, 6):
            raw += pull_star(app_id, country, lang, star, start, RAW_CAP_PER_STAR[star])
        base, boost, in_window = build_sample(raw, start, end, per_cell, seed=week_id)

        existing_ids = set(rev_ws.col_values(1)[1:])
        ts = now_iso()
        rows = [to_row(r, why, week_id, start, week_id, ts) for r, why in base + boost
                if r["reviewId"] not in existing_ids]
        if rows:
            rev_ws.append_rows([[row[c] for c in REVIEW_COLS] for row in rows],
                               value_input_option="RAW")

        status = "done" if len(base) >= min_reviews else "low_volume"
        notes = [] if status == "done" else [f"base sample {len(base)} < {min_reviews}"]
        if PARTIAL:
            notes.append("partial coverage: " + ", ".join(PARTIAL))
        log.update(finished_at=now_iso(), status=status, reviews_fetched=in_window,
                   reviews_new=len(rows), error="; ".join(notes))
        upsert_log(log_ws, log)
        print(f"{week_id}: {in_window} in window, base {len(base)}, boost {len(boost)}, new rows {len(rows)} → {status}")
        if status != "done":
            sys.exit(1)
    except Exception as e:
        log.update(finished_at=now_iso(), status="failed", error=f"{type(e).__name__}: {e}"[:500])
        upsert_log(log_ws, log)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
