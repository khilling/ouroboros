# Experiment 02: Counterfactual xG Attribution — The Crowding Paradox

**Dataset:** StatsBomb WC2022 (5 matches, 114 shots)
**Executed:** 2026-03-17 (v2 — bug-fixed counterfactual indexing)

## Summary

| Metric | Value |
|--------|-------|
| Matches | 5 |
| Shots analyzed | 114 |
| Goals | 11 (9.6%) |
| Off-ball player observations | 566 |

## Fitted xG Model Weights (Logistic Regression)

| Feature | Weight | Interpretation |
|---------|--------|----------------|
| Distance to goal | -0.058 | Closer → higher xG ✓ |
| sin(shot angle) | +2.385 | Wider angle → higher xG ✓ |
| Defenders in cone | +0.066 | More blocking → lower xG ✓ |
| **Teammates in box** | **-0.234** | **Crowding Paradox** |
| Bias | -1.615 | |

## The Crowding Paradox

The negative weight on `teammates_in_box` is the headline finding.

**Interpretation:** When more off-ball attackers crowd the penalty box, defenders position themselves to cover them, narrowing shooting lanes and reducing shot quality per attempt. The highest-value shots occur with fewer box occupants but better shooting geometry.

**Supporting ablation evidence (Exp04):** Shots with 2+ teammates in box have higher Voronoi pitch control (0.178 vs 0.071) — so box presence does create spatial pressure — but the net xG effect is still negative. This suggests the defensive adjustment outweighs the spatial advantage.

## Counterfactual Attribution

Mean per-player, per-shot delta-xG:
- **In-box off-ball players**: Δ = -0.022 (each in-box player hurts expected goals)
- **Out-of-box off-ball players**: Δ ≈ 0.000 (negligible direct effect)

The practical implication: FATE-Score should reward spatial spreading and lane-clearing over box-crowding.

## Bug Fix (v1 → v2)

Original implementation used index-based player removal that referenced position in a filtered list but applied to the full freeze frame. Fixed to use object-identity (`p is not player`). No change to fitted weights (model fitting was unaffected); change affects interpretation of which player's Δ is attributed to whom.
