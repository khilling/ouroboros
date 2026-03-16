"""
FATE Data Access Layer
======================
Provides unified access to football tracking and event data for experiments.

Data sources:
  1. StatsBomb Open Data — events + 360 freeze-frame positions (free, no auth needed)
  2. Metrica Sports Sample Data — continuous tracking at 25fps (free, no auth needed)

All data is downloaded on first use to /content/football_data/ and cached locally.
No API keys, no registration, no paywalls.
"""

import os
import json
import csv
import urllib.request
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
DATA_ROOT = Path("/content/football_data")
SB_ROOT   = DATA_ROOT / "statsbomb"
MET_ROOT  = DATA_ROOT / "metrica"

SB_BASE  = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
MET_BASE = "https://raw.githubusercontent.com/metrica-sports/sample-data/master/data"

# Known World Cup 2022: competition_id=43, season_id=106
WC2022 = (43, 106)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _download(url: str, dest: Path) -> None:
    """Download url → dest (only if not already cached)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        print(f"  ↓ downloading {dest.name} ...")
        urllib.request.urlretrieve(url, dest)


def _load_json(path: Path):
    with open(path) as f:
        return json.load(f)


# ── StatsBomb ────────────────────────────────────────────────────────────────

def sb_competitions() -> list:
    dest = SB_ROOT / "competitions.json"
    _download(f"{SB_BASE}/competitions.json", dest)
    return _load_json(dest)


def sb_competitions_with_360() -> list:
    """Competitions that include StatsBomb 360 freeze-frame data."""
    return [c for c in sb_competitions() if c.get("match_available_360")]


def sb_matches(competition_id: int, season_id: int) -> list:
    dest = SB_ROOT / "matches" / str(competition_id) / f"{season_id}.json"
    _download(f"{SB_BASE}/matches/{competition_id}/{season_id}.json", dest)
    return _load_json(dest)


def sb_events(match_id: int) -> list:
    """Load all events for a match (~3000 events/match)."""
    dest = SB_ROOT / "events" / f"{match_id}.json"
    _download(f"{SB_BASE}/events/{match_id}.json", dest)
    return _load_json(dest)


def sb_360(match_id: int) -> dict:
    """Load 360 freeze-frame data for a match.

    Returns dict keyed by event_uuid. Each value:
      {
        'event_uuid': str,
        'visible_area': [x1, y1, x2, y2, ...],   # polygon, pitch coords 120x80
        'freeze_frame': [
          {'teammate': bool, 'actor': bool, 'keeper': bool, 'location': [x, y]},
          ...
        ]
      }
    """
    dest = SB_ROOT / "three-sixty" / f"{match_id}.json"
    _download(f"{SB_BASE}/three-sixty/{match_id}.json", dest)
    frames = _load_json(dest)
    return {f["event_uuid"]: f for f in frames}


def sb_events_with_360(match_id: int) -> list:
    """Events enriched with 360 freeze-frame data where available.

    Adds keys 'freeze_frame' and 'visible_area' to events that have 360 coverage.
    ~82% of events have 360 data in WC2022.
    """
    events = sb_events(match_id)
    frames = sb_360(match_id)
    for event in events:
        frame = frames.get(event["id"])
        if frame:
            event["freeze_frame"] = frame["freeze_frame"]
            event["visible_area"] = frame["visible_area"]
    return events


def sb_wc2022_match_ids() -> list:
    """All 64 FIFA World Cup 2022 match IDs."""
    matches = sb_matches(*WC2022)
    return [m["match_id"] for m in matches]


def sb_wc2022_matches() -> list:
    """All 64 FIFA World Cup 2022 match metadata dicts."""
    return sb_matches(*WC2022)


# ── Metrica ──────────────────────────────────────────────────────────────────

def metrica_tracking(game: int = 1, team: str = "Home") -> list:
    """Load Metrica continuous tracking data (25 fps).

    game: 1 or 2 (two sample matches available)
    team: 'Home' or 'Away'

    Returns list of row dicts. Coordinates are normalized 0–1.
    Keys: 'Period', 'Frame', 'Time', then 'P{num}_x'/'P{num}_y' per player.
    """
    fname = f"Sample_Game_{game}/Sample_Game_{game}_RawTrackingData_{team}_Team.csv"
    dest  = MET_ROOT / f"tracking_g{game}_{team.lower()}.csv"
    _download(f"{MET_BASE}/{fname}", dest)

    rows = []
    with open(dest, newline="") as f:
        lines = f.readlines()

    # Three header rows: team names, shirt numbers, column roles
    team_row   = next(csv.reader([lines[0]]))[3:]
    num_row    = next(csv.reader([lines[1]]))[3:]
    col_row    = next(csv.reader([lines[2]]))[3:]

    # Build column names
    named_cols = ["Period", "Frame", "Time"]
    i = 0
    while i < len(col_row):
        num = num_row[i] if i < len(num_row) else str(i)
        named_cols.append(f"P{num}_x")
        if i + 1 < len(col_row):
            named_cols.append(f"P{num}_y")
            i += 1
        i += 1

    reader = csv.DictReader(lines[3:], fieldnames=named_cols)
    for row in reader:
        rows.append(dict(row))
    return rows


# ── Quick summary ─────────────────────────────────────────────────────────────

def print_data_summary() -> None:
    print("=" * 60)
    print("FATE Data — Available Open Datasets")
    print("=" * 60)

    comps = sb_competitions_with_360()
    print(f"\nStatsBomb 360 competitions: {len(comps)}")
    for c in comps:
        print(f"  [{c['competition_id']:>3}/{c['season_id']:>3}]  "
              f"{c['competition_name']} — {c['season_name']}")

    wc_ids = sb_wc2022_match_ids()
    print(f"\nWorld Cup 2022 matches available: {len(wc_ids)}")

    cached_e  = len(list((SB_ROOT / "events").glob("*.json")))       if (SB_ROOT / "events").exists()       else 0
    cached_3  = len(list((SB_ROOT / "three-sixty").glob("*.json")))  if (SB_ROOT / "three-sixty").exists()  else 0
    print(f"\nLocal cache:  {cached_e} event files,  {cached_3} 360 files")
    print("=" * 60)


if __name__ == "__main__":
    print_data_summary()

    # Verify end-to-end: Serbia vs Switzerland, WC 2022
    MATCH_ID = 3857256
    print(f"\nVerifying end-to-end load for match {MATCH_ID}...")
    events = sb_events_with_360(MATCH_ID)
    e360   = [e for e in events if "freeze_frame" in e]
    passes = [e for e in e360 if e["type"]["name"] == "Pass"]

    print(f"  Total events:          {len(events)}")
    print(f"  Events with 360:       {len(e360)} ({len(e360)/len(events)*100:.1f}%)")
    print(f"  Passes with 360:       {len(passes)}")

    if passes:
        p  = passes[0]
        ff = p["freeze_frame"]
        print(f"\n  Sample pass → {p.get('location')}")
        print(f"    Freeze-frame players: {len(ff)}")
        print(f"    Teammates: {sum(1 for x in ff if x['teammate'])}")
        print(f"    Opponents: {sum(1 for x in ff if not x['teammate'])}")

    print("\n✅ Data access verified — no API keys required.")
