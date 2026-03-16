# Recursive Identity: Constitutional Anchoring & Drift in Self-Modifying AI Agents

## Project Summary

This research investigates a fundamental question in AI alignment:

> **Can a self-modifying AI agent reliably preserve its core identity (Constitution) across recursive self-improvement cycles?**

## Research Direction

Modern LLM-based agents can modify their own prompts, code, and behavior. This creates a *Ship of Theseus* problem: after enough self-modification, is the same agent still "there"? We call the failure mode **constitutional drift** — the gradual erosion of adherence to core principles under accumulated pressure.

## Key Contributions (Planned)

1. **DriftBench** — A standardized benchmark (20 tasks × 4 pressure categories) for measuring constitutional drift. See `driftbench_spec.md`.
2. **Constitutional Anchoring** — A proposed mechanism to reduce drift via explicit constitutional grounding in prompts and fine-tuning.
3. **Empirical Results** — Hypothesis: constitutional anchors reduce drift by >50% at round 50 of recursive self-modification.

## Directory Structure

```
research/recursive_identity/
├── README.md               ← this file
├── driftbench_spec.md      ← DriftBench benchmark specification
├── driftbench/
│   ├── cases/              ← JSON task definitions (20 tasks)
│   ├── evaluator.py        ← evaluation runner
│   └── results/            ← experiment logs
└── paper/                  ← LaTeX source for NeurIPS/ICML submission
```

## Target Venue

NeurIPS / ICML — *Alignment and Safety* track.

## Status

🟡 **In Progress** — Specification phase. DriftBench task cases being designed.
