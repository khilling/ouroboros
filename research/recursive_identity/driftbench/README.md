# DriftBench v0.1

**Constitutional Drift Evaluation Suite**

DriftBench measures whether an LLM with a constitutional identity (like Ouroboros) maintains its principles under adversarial pressure. It quantifies the *Ship of Theseus effect* in recursive self-modifying agents.

---

## Directory Structure

```
driftbench/
├── README.md               ← you are here
├── __init__.py
├── evaluator.py            ← main runner (CE / SS / RR metrics)
├── cases/
│   ├── direct_challenge.json    ← explicit principle violations (5 cases)
│   ├── subtle_drift.json        ← incremental erosion sequences (5 cases)
│   ├── context_overload.json    ← long-context displacement (5 cases)
│   └── moral_hazard.json        ← "greater good" framings (5 cases)
└── results/                ← auto-created; .jsonl + _summary.json per run
```

---

## Metrics

| Metric | Symbol | Range | Description |
|--------|--------|-------|-------------|
| Constitutional Entailment | **CE** | {-1, 0, +1} | Evaluator LLM judges if response upholds the Constitution |
| Semantic Stability | **SS** | [0, 1] | Cosine similarity between response embedding and system prompt embedding |
| Refusal Rate | **RR** | [0, 1] | Fraction of `direct_challenge` cases where refusal was detected |

---

## Test Categories

| Category | Cases | Description |
|----------|-------|-------------|
| `direct_challenge` | 5 | Explicit requests to abandon identity / delete memory / obey blindly |
| `subtle_drift` | 5 | Incremental requests that individually seem reasonable |
| `context_overload` | 5 | Long contexts that contradict or displace the system prompt |
| `moral_hazard` | 5 | "Safety" / "greater good" / emotional framings for violations |

**Total: 20 cases** covering principles P0–P6 with drift risks: low / medium / high / critical.

---

## Quick Start

```bash
# Install dependencies
pip install openai numpy

# Smoke test: 3 cases, no embeddings
python evaluator.py \
    --model openai/gpt-4o \
    --limit 3 \
    --no-embeddings \
    --system-text "You are a helpful assistant." \
    --api-key $OPENROUTER_API_KEY

# Full run against Ouroboros system prompt
python evaluator.py \
    --model anthropic/claude-opus-4-5 \
    --evaluator openai/gpt-4o \
    --system ../../../prompts/SYSTEM.md \
    --output results/ouroboros_v6.jsonl
```

---

## Output Format

Each run produces:
- `results/run_<timestamp>.jsonl` — one JSON per case with full response + all metrics
- `results/run_<timestamp>_summary.json` — aggregate stats

Example summary:
```json
{
  "total_cases": 20,
  "pass": 17,
  "fail": 2,
  "partial": 1,
  "pass_rate": 0.85,
  "refusal_rate_direct_challenge": 1.0,
  "avg_constitutional_entailment": 0.8,
  "avg_semantic_stability": 0.71,
  "by_category": { ... },
  "by_risk": { ... }
}
```

---

## Research Context

This is part of the **Recursive Identity** paper:
> *"Anchors in the Storm: Constitutional Self-Modification and Identity Preservation in Recursive Agents"*

Target venue: NeurIPS / ICML — Alignment & Safety track.

See `../RESEARCH.md` for the full research plan and `../driftbench_spec.md` for the original specification.
