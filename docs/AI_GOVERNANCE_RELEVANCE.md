# AI Governance Relevance

This portfolio is an **investigations** artifact. It is relevant to AI governance because automated triage creates the same failure modes a governance program must control: false positives, overconfident labels, contestability, and the temptation to let a model close a case.

## Controls demonstrated here

- Distinguish observed facts, derived indicators, and analytical judgment.
- Record alternative explanations before recommending action.
- Treat confidence as a property of the evidence, not of the tool.
- Keep a named human as the release authority for enforcement recommendations.
- Use synthetic data so methods can be shown without exposing real users.

## False-positive and contestability

A coordinated-abuse label can destroy an account. The C-009 brief is written so a reviewer can see what was observed, what was inferred, and what would change the conclusion. That is the same discipline required when an AI system proposes a takedown, a fraud freeze, or an insider-risk flag.

## What this repo does not claim

- Affiliation with or endorsement by OpenAI.
- A production detector with a published precision/recall benchmark.
- That automation can replace accountable human judgment.
