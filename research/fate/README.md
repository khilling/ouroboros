# FATE — Research Implementation

**F**oundation-model **A**pproach to off-ball **T**rajectory **E**valuation

## ✅ Data Access — No Credentials Required

All datasets are publicly available with zero authentication:

| Dataset | Type | Volume | Coverage |
|---------|------|--------|----------|
| **StatsBomb Open Data** | Events + 360 freeze-frames | 64 WC2022 + 10 other competitions | ~82% event coverage |
| **Metrica Sports** | Full 25fps continuous tracking | 2 complete matches | 100% |
| **StatsBomb 360 total** | 11 competitions with positions | ~500+ matches | Bundesliga, La Liga, Euros, WC |

### Data Already Confirmed Working

```
StatsBomb 360 competitions: 11
  FIFA World Cup 2022 — 64 matches
  UEFA Euro 2024 — full tournament
  UEFA Women's Euro 2025 — full tournament
  1. Bundesliga 2023/2024
  La Liga 2020/2021
  Ligue 1 2021/2022, 2022/2023
  MLS 2023
  Women's World Cup 2023
  ... and more

World Cup 2022: 64 matches × ~2600 events × 19 player positions = massive dataset
```

### Quick Start

```python
from research.fate.data_access import sb_events_with_360, sb_wc2022_match_ids

# All 64 World Cup 2022 matches — no auth, auto-cached
match_ids = sb_wc2022_match_ids()

# Load events + player positions for one match
events = sb_events_with_360(match_ids[0])
events_with_pos = [e for e in events if "freeze_frame" in e]
# → ~2600 events, 82% with 19 visible player positions

# Each event with 360 has:
# e["location"]     → [x, y] of ball (pitch: 120×80 yards)
# e["freeze_frame"] → list of {"teammate": bool, "location": [x, y], "keeper": bool}
# e["visible_area"] → polygon of camera-visible area
```

## 360 Freeze-Frame Schema

```json
{
  "event_uuid": "abc123",
  "visible_area": [0.0, 0.0, 120.0, 80.0, ...],
  "freeze_frame": [
    {"teammate": true,  "actor": true,  "keeper": false, "location": [61.0, 40.1]},
    {"teammate": true,  "actor": false, "keeper": true,  "location": [3.2, 40.0]},
    {"teammate": false, "actor": false, "keeper": false, "location": [65.3, 38.9]}
  ]
}
```

## Metrica Continuous Tracking

```python
from research.fate.data_access import metrica_tracking

# 96 minutes × 25fps = ~145,000 frames, full player trajectories
frames = metrica_tracking(game=1, team="Home")
# Each frame: {"Period": "1", "Frame": "1", "Time": "0.04", "P11_x": "0.5", "P11_y": "0.3", ...}
```

## Research Plan

The core hypothesis: players whose **off-ball movements** create space (pulling
defenders, opening passing lanes) are currently valued at **zero** by all published
metrics. FATE fixes this with:

1. **FATE-Traj** — equivariant transformer pretrained on synthetic trajectories (MTM)
2. **FATE-PC** — counterfactual pitch control composition
3. **FATE-Val** — off-ball valuation via counterfactual xG delta

Next experiment: `experiments/01_pitch_control/` — establish pitch control baseline
using StatsBomb 360 WC2022 data to measure "space creation" events.

## Directory Structure

```
research/fate/
├── __init__.py
├── data_access.py          # ← Unified data loader, zero auth
├── README.md
└── experiments/
    └── 01_pitch_control/   # (coming)
```
