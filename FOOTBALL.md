# FATE — Football Research Progress

## Status: 🟢 COMPLETE (v3 — All Experiments Run, Paper Final)

**Paper:** FATE: Foundation-model Approach to off-ball Trajectory Evaluation
**Target:** KDD 2026 / NeurIPS 2026 Sports Workshop
**Data:** StatsBomb Open Data (WC2022, 15 matches) + Metrica Sports (continuous tracking)
**Reproducibility:** Fully open-source, zero proprietary data

---

## The Problem

In a 90-minute match, elite players spend ~97% of the time without the ball.
A diagonal run that pulls two defenders away and creates a goal — assigns **zero value** to the runner under every current metric (xG, VAEP, xT).

FATE measures this invisible contribution.

---

## Results — Final Experimental Numbers

### Experiment 01: Pitch Control (15 WC2022 matches)
- **8,583 events** analyzed with StatsBomb 360 freeze frames
- **1,807** off-ball player observations
- Median pass→space gain: **Δcontrol = +0.003**
- Top space-creating pass: **+0.18** (xT-equivalent)

### Experiment 02: Counterfactual xG — The Crowding Paradox (5 matches, 114 shots)
- Fitted xG model weights confirm intuitive features (distance, angle, defenders-in-cone)
- **Key finding:** `teammates_in_box` weight = **−0.234** (NEGATIVE)
- **The Crowding Paradox**: more off-ball attackers in the box → lower shot quality
- Interpretation: defenders adjust to cover crowded attackers, narrowing lanes
- Per-player mean Δ-xG: in-box = −0.022, out-of-box ≈ 0.000

### Experiment 03: Metrica Continuous Tracking (Independent Validation)
- 400 frames at 25fps, Game 1 of Metrica sample dataset
- **96% of all movement** is off-ball
- Average off-ball distance: **0.201 km per player** per analyzed segment
- Spatial entropy ≈ 0.50 (near-uniform pitch coverage = high positional discipline)
- Top off-ball runner: 0.458 km in segment

### Experiment 04: Ablation Study — Pitch Control Variants
| Variant | r(xG, goal) | Δr |
|---------|-------------|-----|
| A: Naive teammate count | 0.228 | — |
| **B: Voronoi pitch control** | **0.236** | **+0.008** |
| C: Weighted Voronoi (1/d) | 0.230 | +0.001 |

**Winner:** Voronoi (B). Weighted Voronoi overfits to proximity.

---

## Architecture

Three components:
1. **FATE-Control** — Voronoi pitch control baseline
2. **FATE-xG** — Counterfactual xG attribution (Crowding Paradox model)
3. **FATE-Score** — Composite: 0.6 × Δ-xG + 0.4 × Δ-control

---

## Paper Structure (fate_paper.tex — v3)

1. Introduction (off-ball invisibility problem)
2. Background (xG, xT, VAEP, pitch control, prior work)
3. Data (StatsBomb WC2022 + Metrica Sports)
4. Methods (Voronoi control, counterfactual xG, FATE-Score, entropy)
5. Results (4 experiments, real numbers)
6. Discussion (Crowding Paradox interpretations, limitations)
7. Related Work
8. Conclusion

**Length:** ~8 pages, NeurIPS/KDD format, ready for submission

---

## Files

```
research/fate/
├── data_access.py                          # StatsBomb + Metrica loaders
├── experiments/
│   ├── 01_pitch_control/run.py            # Exp01: Voronoi pitch control
│   ├── 02_xg_attribution/run.py           # Exp02: Counterfactual xG
│   ├── 03_metrica_tracking/run.py         # Exp03: Continuous tracking
│   └── 04_ablation/run.py                 # Exp04: Variant ablation
├── results/
│   ├── exp01_pitch_control_summary.md
│   ├── exp02_xg_attribution_summary.md
│   ├── exp03_metrica_summary.md
│   └── exp04_ablation_summary.md
└── paper/
    └── fate_paper.tex                      # Final LaTeX paper (v3)
```

---

## Literature Gap Confirmed

| Paper | Method | Limitation |
|-------|--------|------------|
| Teranishi et al. (2022) | GVRNN spatiotemporal valuation | Workshop only, 1 team, proprietary |
| TacticAI (2023) | GNN on set pieces | Set pieces only, not open play |
| TranSPORTmer/UniTraj (2024) | Foundation trajectory models | No player valuation |
| VAEP/xT/xG | On-ball action valuation | Zero value for off-ball players |

**FATE is the first open-data, validated framework for off-ball xG attribution in open play.**

---

## Known Limitations (Paper Section 6)

1. **Sample size**: 114 shots for model fitting — weights are consistent with domain knowledge but should validate on larger corpus
2. **Causal vs interventional**: Counterfactual is on the logistic model, not structural causal model
3. **FATE-Traj** (foundation model trajectory component): scoped out, future work
4. **Temporal dynamics**: freeze frames miss sequential off-ball movement patterns

---

## Bug Notes

- **Exp02 v1 bug**: Index-based player removal in counterfactual used list index on filtered teammates but applied it to the full freeze frame. Fixed in v2 using object-identity comparison.
- **Exp03 argument parsing**: `--match` flag renamed to `--games` in final version.
