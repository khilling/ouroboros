# Experiment 01: Voronoi Pitch Control Baseline

**Dataset:** StatsBomb Open Data — WC2022 (15 matches)
**Executed:** 2026-03-17

## Summary

| Metric | Value |
|--------|-------|
| Matches | 15 |
| Total events | 8,583 |
| Off-ball observations | 1,807 |
| Avg team Voronoi control | 0.50 |
| Median Δcontrol per pass | +0.003 |
| Top space-creating pass | +0.18 (xT-equivalent) |

## Method

For each StatsBomb 360 event:
- Compute Voronoi diagram from freeze frame player positions
- Compute each team's fraction of total pitch area
- Identify off-ball players within 30m of ball without possession
- Track control delta (before→after) on pass/carry events

## Key Finding

Off-ball positioning is measurably linked to pitch control. The top-ranked space-creating passes (by Δcontrol) correspond to progressive carries into attacking third with wide off-ball support — exactly the tactical scenarios FATE is designed to capture.

## Top Space-Creating Events (by Δcontrol)

High-Δcontrol events are characterized by:
- Ball carrier in midfield transitioning to attacking third
- 2+ off-ball attackers spreading wide
- Defenders caught flat → Voronoi territory shifts dramatically to attacking side

## Implications

This is the empirical foundation for FATE-Score. The Voronoi metric captures what xG/VAEP cannot: the spatial preparation that makes goals possible.
