"""Scrape the public contribution calendar. No token, no API quota."""
import json, os, re, sys
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_USER") or (sys.argv[1] if len(sys.argv) > 1 else "SoansSandha")
URL = f"https://github.com/users/{USER}/contributions"

def fetch():
    r = requests.get(URL, headers={"User-Agent": "profile-readme-art"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tips = {t.get("for"): t.get_text(strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        text = tips.get(td.get("id"), "")
        m = re.match(r"(\d+)\s+contribution", text)
        days.append({
            "date": td["data-date"],
            "level": int(td.get("data-level", 0)),
            "count": int(m.group(1)) if m else 0,
        })
    days.sort(key=lambda d: d["date"])
    if not days:
        raise SystemExit("No contribution cells found; GitHub markup may have changed.")
    return days

def stats(days):
    today = date.today()
    counts = {date.fromisoformat(d["date"]): d["count"] for d in days}
    total = sum(counts.values())
    longest = run = 0
    for d in sorted(counts):
        run = run + 1 if counts[d] else 0
        longest = max(longest, run)
    # current streak: walk back from today (or yesterday if today is still empty)
    cur, d = 0, today
    if not counts.get(d):
        d -= timedelta(days=1)
    while counts.get(d):
        cur += 1
        d -= timedelta(days=1)
    best_date = max(counts, key=lambda k: counts[k])
    months = {}
    for d, c in counts.items():
        months[d.strftime("%Y-%m")] = months.get(d.strftime("%Y-%m"), 0) + c
    return {
        "total": total, "current_streak": cur, "longest_streak": longest,
        "best_day": {"date": best_date.isoformat(), "count": counts[best_date]},
        "months": dict(sorted(months.items())),
    }

if __name__ == "__main__":
    days = fetch()
    out = {"user": USER, "days": days, "stats": stats(days)}
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"{USER}: {out['stats']['total']} contributions, {len(days)} days")
