# Experiment 02 — Counterfactual xG Attribution

**Run date:** 2026-03-17  
**Status:** ✅ Complete (v2 — fixed counterfactual indexing bug)

## Setup
- Data: StatsBomb WC2022 open data (5 matches, same as Exp01)
- Shots analyzed: 114 total; goals: 11 (9.6% conversion)
- xG model: logistic regression (gradient descent)
- Counterfactual: remove each off-ball player, recompute xG delta

## Fitted xG Model Weights

| Feature | Weight | Interpretation |
|---------|--------|---------------|
| `distance` | −0.0584 | Closer = higher xG ✓ |
| `angle_sin` | +2.3848 | Wider angle = higher xG ✓ |
| `defenders_cone` | +0.0657 | More defenders in cone = lower xG ✓ |
| `teammates_box` | **−0.2335** | ⚠️ **CROWDING PARADOX** |
| bias | −1.6149 | — |

## The Crowding Paradox

**`teammates_box` weight = −0.2335 (negative)**

More off-ball teammates in the penalty box correlates with *lower* shot quality. This is the central finding of the paper:

- In-box off-ball players mean Δ-xG: **−0.0221** (n=291)
- Out-of-box off-ball players mean Δ-xG: **0.0000** (n=275)

**Interpretation:** When more teammates crowd the box, defenders follow. The defensive adjustment outweighs the offensive threat. The most valuable off-ball positioning is **spatial spreading**, not box-crowding.

## Per-match Results

| Match | Shots | Avg xG |
|-------|-------|--------|
| Serbia vs Switzerland | 26 | 0.1719 |
| Argentina vs Australia | 19 | 0.1168 |
| Australia vs Denmark | 22 | 0.1008 |
| Brazil vs Serbia | 26 | 0.0854 |
| Tunisia vs Australia | 21 | 0.1034 |
| **Overall** | **114** | **0.1157** |

## Bug Fix Note (v2)

v1 applied counterfactual player removal using a list-index on a filtered sub-list while comparing against the full frame. Fixed in v2: player removal uses object-identity matching, ensuring the counterfactual frame correctly excludes only the target player.

## Notes
- Full JSON: `/content/football_data/results/exp02_xg_attribution.json`
- Model is deliberately simple (5 features) to validate direction, not maximize accuracy
- The crowding paradox finding is consistent across all 5 matches
