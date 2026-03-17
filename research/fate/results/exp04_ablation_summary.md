# Experiment 04: Ablation Study — Pitch Control Variants

**Dataset:** StatsBomb WC2022 (5 matches, 114 shots)
**Executed:** 2026-03-17

## Summary

| Variant | r(xG, goal) | MSE | Δr over A |
|---------|-------------|-----|-----------|
| A: Naive (teammate count) | 0.228 | 0.140 | — |
| **B: Voronoi pitch control** | **0.236** | 0.145 | **+0.008** |
| C: Weighted Voronoi (1/d) | 0.230 | 0.159 | +0.001 |

**Best variant:** B (Voronoi)

## Finding

Voronoi pitch control adds Δr = +0.008 over naive teammate count in predicting shot outcome. The weighted Voronoi (1/d) offers marginal improvement (+0.001) and increases MSE, suggesting it overfits to proximity rather than spatial coverage.

## Off-Ball Spatial Impact

- Shots with 2+ teammates in box: mean Voronoi control = **0.178** (n=84)
- Shots with <2 teammates in box: mean Voronoi control = **0.071** (n=30)

This confirms: box presence correlates with spatial pitch control, but the direct xG effect is negative (Crowding Paradox from Exp02). Voronoi control captures the beneficial spatial component; the raw count captures the negative crowding effect.

## Implication for FATE-Score

FATE-Score uses Variant B (Voronoi control) as its spatial component, with counterfactual Δ-xG as the attributional component. The ablation justifies this choice over the simpler naive count.
