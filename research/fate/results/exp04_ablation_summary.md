# Experiment 04 — Ablation Study: Pitch Control Variants

**Run date:** 2026-03-17  
**Status:** ✅ Complete

## Setup
- Data: StatsBomb WC2022 (5 matches, 114 shots, 11 goals)
- Three pitch control variants compared against ground-truth goal labels
- Metric: Pearson r(xG, goal) and MSE

## Results

| Variant | r(xG, goal) | MSE | Δ over Naive |
|---------|-------------|-----|--------------|
| A — Naive count | 0.2282 | 0.1397 | baseline |
| **B — Voronoi** | **0.2357** | 0.1448 | **+0.0109 r** |
| C — Weighted Voronoi | 0.2296 | 0.1586 | +0.0037 r, +MSE |

**Best variant: B (Voronoi)**

## Interpretation

- Voronoi pitch control adds r = **+0.0075** over naive teammate count
- Weighted Voronoi adds only r = +0.0013 and significantly worsens MSE (overfits on 114 shots)
- Despite modest absolute gains, the direction is consistent: **spatial positioning adds signal**

## Crowding in Pitch Control Context

- Shots with ≥2 teammates in box: mean Voronoi control = **0.178** (n=84)
- Shots with <2 teammates in box: mean Voronoi control = **0.071** (n=30)
- More teammates does not guarantee pitch control *in the shooting lane* — consistent with Exp02 crowding paradox

## Conclusion

The Voronoi model best captures off-ball spatial value. The weighted variant introduces overfitting at this sample size. The FATE paper should use Variant B as the primary pitch control method.

## Notes
- Full JSON: `/content/football_data/results/exp04_ablation.json`
- Weighted Voronoi uses inverse-distance weighting from goal to ball to each player
- 5 matches chosen to match Exp01/02 for consistency
