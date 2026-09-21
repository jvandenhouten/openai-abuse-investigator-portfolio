# Abuse Investigation & Detection Portfolio

**Synthetic investigations | SQL | Python | Cross-case network analysis | Human-reviewed conclusions**

This independent professional portfolio shows how investigative judgment, intelligence analysis, relational data, and technical tooling can be combined to assess violent threats, coordinated abuse, enforcement evasion, and false positives.

> **Important:** All cases, users, targets, devices, infrastructure, content, and events are fictional and synthetically generated. **This project is not affiliated with or endorsed by OpenAI.** The repository name is a historical portfolio label for a target role. It contains no real user information and no operationally useful harmful instructions.

**AI governance note:** [docs/AI_GOVERNANCE_RELEVANCE.md](docs/AI_GOVERNANCE_RELEVANCE.md)

## Live dashboard

[Abuse Investigation & Detection Dashboard](https://joel-abuse-investigation-portfolio.streamlit.app)

## Status (2026-09-21)

**Featured case complete:** C-009 deep-dive (brief, SQL, notebook, charts).
**Dataset complete:** 10 synthetic cases and supporting relational tables.
**Roadmap (not finished — do not cite as delivered):** remaining nine case briefs, portfolio-wide network model, detection evaluation report, public website.

CI runs dataset integrity tests on every push.

## Dataset (synthetic)

- 10 interrelated investigations
- 158 fictional accounts
- 3,010 platform events
- 1,989 content-metadata records
- 533 sessions
- 51 reports and enforcement actions
- 15 case-to-case links
- 136 account-to-account links

## Featured investigation: C-009

**Cross-Regional Harassment Network Using Shared Infrastructure**

C-009 demonstrates cross-case entity resolution, shared-device analysis, repeated-content detection, post-enforcement assessment, role differentiation, timeline analysis, competing hypotheses, and confidence-rated recommendations.

- `case_briefs/C-009_Case_Brief.md`
- `notebooks/C009_investigation_analysis.ipynb`
- `scripts/analyze_c009.py`
- `sql/C009_investigation_queries.sql`

## Analytical standards

Every case product distinguishes:

- observed facts
- derived indicators
- analytical judgments
- alternative explanations
- confidence assessments
- recommended action
- limitations and collection gaps

Automation supports triage and pattern discovery. It does not replace accountable human judgment.

## Local setup

```bash
git clone https://github.com/jvandenhouten/openai-abuse-investigator-portfolio.git
cd openai-abuse-investigator-portfolio
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
python -m pytest tests/ -q
```

## Author

**Joel L. Vandenhouten**
Retired U.S. Army Major | Intelligence, Investigations, Corporate Security, Crisis Operations
Texas A&M University School of Law — Master of Legal Studies candidate, Cybersecurity Law & Policy
