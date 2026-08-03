# C-009 Investigative Case Brief

## Cross-Regional Harassment Network Using Shared Infrastructure

> **Synthetic portfolio case.** All accounts, targets, devices, infrastructure, content, and events are fictional.  
> This analysis is an independent professional portfolio project and is not affiliated with or endorsed by OpenAI.

## Executive Assessment

**Assessment:** C-009 is a high-confidence coordinated account network exhibiting shared infrastructure,
cross-case account overlap, repeated content families, post-enforcement behavior, functional role differentiation,
and language obfuscation.

**Analytical confidence:** High  
**Evidence sufficiency score:** 100.0/100  
**Ground-truth label:** True Positive - Coordinated Network

The available synthetic evidence is more consistent with an organized network than with unrelated users
independently engaging in similar conduct. The strongest linkage is to C-003, followed by C-002, C-008,
C-007, and C-001.

## Scope

- **Primary accounts:** 27
- **Events analyzed:** 450
- **Directly linked cases:** 5
- **Cross-case accounts:** 5
- **Cross-case shared devices:** 4
- **Cross-case reused content hashes:** 18
- **Recorded triage actions:** 9
- **Median triage time:** 29 minutes

## Principal Findings

### 1. Cross-case account overlap

Five C-009 accounts also appear in C-001, C-002, C-003, C-007, or C-008. Each is marked as previously
enforced and high risk in the synthetic dataset. This overlap materially reduces the likelihood that the cases
are wholly independent.

### 2. Shared infrastructure

Four devices connect C-009 activity to other investigations:

- DEV-X05: C-003, C-006, C-008, and C-009
- DEV-X01: C-001, C-007, and C-009
- DEV-X03: C-002 and C-009
- DEV-X10: C-008 and C-009

Infrastructure sharing alone is not conclusive because devices and networks can be shared legitimately.
Here, however, it aligns with cross-case accounts, repeated content, prior enforcement, and role-based behavior.

### 3. Repeated content families

Eighteen content hashes found in C-009 also appear in another synthetic case. Several recur across C-003,
C-004, and C-009, while other families link C-009 to either C-003 or C-004. The content is represented through
safe placeholders, so the analytical value lies in recurrence, sequence, and case distribution rather than wording.

### 4. Functional role differentiation

The network contains four recurring roles:

| Role | Accounts | Events | Average Risk |
|---|---:|---:|---:|
| controller | 7 | 125 | 0.724 |
| amplifier | 8 | 115 | 0.685 |
| infrastructure_helper | 6 | 111 | 0.696 |
| replacement_account | 6 | 99 | 0.687 |

Controllers generate the highest average synthetic risk score. Amplifiers produce substantial event volume,
while infrastructure helpers and replacement accounts support persistence and network continuity.

### 5. Direct case relationships

| Linked Case | Relationship | Strength | Evidence Items |
|---|---|---:|---:|
| C-003 | post enforcement evasion | 0.91 | 11 |
| C-002 | shared content and roles | 0.88 | 9 |
| C-008 | evasion and role network | 0.87 | 9 |
| C-007 | template and infrastructure | 0.85 | 8 |
| C-001 | shared infrastructure | 0.79 | 7 |

## Competing Hypotheses

### H1 - Coordinated network
Supported by cross-case accounts, shared devices, repeated content families, prior enforcement, specialized
roles, and five high-confidence case relationships.

### H2 - Coincidental parallel behavior
Possible in isolation, especially for common devices, networks, or language. It is less persuasive when all
linkage types are considered together.

### H3 - Shared legitimate environment
A workplace, household, or public access point could explain some infrastructure overlap. The synthetic record
does not contain corroborating evidence of a benign shared environment, and the role and enforcement patterns
weaken this explanation.

### H4 - Detection artifact
Repeated safe placeholders and generated content families could inflate similarity. For that reason, content
similarity is treated as corroboration rather than the sole basis for the assessment.

## Recommended Actions

1. Treat C-009 and its five directly linked cases as a coordinated investigative cluster.
2. Preserve account, device, session, content-family, target, and enforcement-link evidence.
3. Prioritize previously enforced accounts and controller roles for human review.
4. Apply proportionate network-level restrictions after validating account ownership and context.
5. Develop reusable detection features for cross-case account membership, shared infrastructure, template
   recurrence, role differentiation, and post-enforcement reappearance.
6. Require analyst review before enforcement when infrastructure or content similarity is the only linkage.
7. Measure false positives against C-010 and mixed-ground-truth cases C-005 and C-007.

## Limitations

- The dataset is synthetic and intentionally contains discoverable ground-truth relationships.
- Content is represented by safe placeholders rather than natural language.
- Device and network-sharing can have benign explanations.
- Risk scores are synthetic features, not validated production-model outputs.
- No automated score should be treated as an enforcement decision.

## Conclusion

The converging evidence supports the assessment that C-009 is a coordinated cross-regional network with
persistent links to five other investigations. The most probative findings are cross-case account overlap,
multi-case device reuse, post-enforcement indicators, recurring content families, and differentiated network roles.
The case demonstrates how SQL, Python, network analysis, and human investigative judgment can be combined
without allowing automation to replace accountable decision-making.
