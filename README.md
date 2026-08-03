# Abuse Investigation & Detection Portfolio

**Synthetic investigations | SQL | Python | Codex-assisted workflows | Cross-case network analysis**

This independent professional portfolio demonstrates how investigative judgment, intelligence analysis,
relational data, and technical tooling can be combined to identify and assess violent threats,
coordinated abuse, enforcement evasion, extremist activity, and false positives.

> **Important:** All cases, users, targets, devices, infrastructure, content, and events in this repository
> are fictional and synthetically generated. This project is not affiliated with or endorsed by OpenAI.
> It contains no real user information and no operationally useful harmful instructions.

## Live Interactive Dashboard

[Open the Abuse Investigation & Detection Dashboard](https://joel-abuse-investigation-portfolio.streamlit.app)

## Project Status

**Phase 3 in progress - C-009 deep-dive investigation completed**

Current repository components:

- 10 interrelated synthetic investigations
- 158 fictional accounts
- 3,010 synthetic platform events
- 1,989 safe content-metadata records
- 533 sessions
- 51 reports and enforcement actions
- 15 case-to-case links
- 136 account-to-account links
- SQLite database and CSV exports
- SQL investigation pack
- Streamlit case explorer and C-009 deep dive
- Python C-009 analysis script and notebook
- C-009 investigative case brief
- Documented safety, privacy, and human-review principles

## Featured Investigation: C-009

**Cross-Regional Harassment Network Using Shared Infrastructure**

C-009 demonstrates cross-case entity resolution, shared-device analysis, repeated-content detection,
post-enforcement assessment, role differentiation, timeline analysis, competing hypotheses, and
confidence-rated recommendations.

Key synthetic findings:

- 27 primary accounts and 450 events
- 5 accounts linked to another case
- 4 devices connecting C-009 to other cases
- 18 content hashes reused beyond C-009
- 5 direct high-confidence case relationships
- 4 differentiated network roles

Files:

- `case_briefs/C-009_Case_Brief.md`
- `case_briefs/C-009_Case_Brief.pdf`
- `notebooks/C009_investigation_analysis.ipynb`
- `scripts/analyze_c009.py`
- `sql/C009_investigation_queries.sql`
- `assets/c009_case_network.png`
- `assets/c009_activity_timeline.png`

## Investigative Questions

1. Which apparently separate cases share accounts, devices, network infrastructure, targets, or content templates?
2. Which clusters show synchronized or burst activity?
3. How can an analyst distinguish coordinated abuse from lawful coordination?
4. Which accounts appear to perform specialized roles within a network?
5. What evidence suggests post-enforcement evasion?
6. Which findings are strong enough to support action, and which require further collection?
7. How should automated findings be validated before an investigative conclusion is reached?

## Repository Structure

```text
.
├── app.py
├── requirements.txt
├── assets/
├── case_briefs/
├── data/
├── database/
├── docs/
├── notebooks/
├── reports/
├── scripts/
└── sql/
```

## Run the Dashboard Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Use the SQLite Database

```bash
sqlite3 database/openai_abuse_investigator_synthetic.sqlite
```

Example:

```sql
SELECT case_id, case_title, severity, ground_truth_label
FROM cases
ORDER BY case_id;
```

## Analytical Standards

Every case product distinguishes among:

- observed facts
- derived indicators
- analytical judgments
- alternative explanations
- confidence assessments
- recommended action
- limitations and collection gaps

Automation supports triage and pattern discovery; it does not replace accountable human judgment.

## Planned Deliverables

- [x] Case taxonomy and cross-case pattern library
- [x] Synthetic relational dataset
- [x] Initial SQL investigation pack
- [x] Interactive case explorer
- [x] C-009 Python and SQL deep-dive analysis
- [x] C-009 investigative case brief
- [ ] Complete Python feature-engineering notebook
- [ ] Portfolio-wide cross-case network model
- [ ] Remaining nine investigative case briefs
- [ ] Detection methodology and evaluation report
- [ ] Executive intelligence report
- [ ] Public portfolio website

## Author

**Joel L. Vandenhouten**  
Retired U.S. Army Major | Intelligence, Investigations, Corporate Security, Crisis Operations  
Texas A&M University School of Law - Master of Legal Studies candidate, Cybersecurity Law & Policy

This project is an independent professional portfolio using wholly synthetic data.
