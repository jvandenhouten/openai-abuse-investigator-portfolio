# Abuse Investigation & Detection Portfolio

**Synthetic investigations | SQL | Python | Codex-assisted workflows | Cross-case network analysis**

This independent professional portfolio demonstrates how investigative judgment, intelligence analysis,
relational data, and technical tooling can be combined to identify and assess violent threats,
coordinated abuse, enforcement evasion, extremist activity, and false positives.

> **Important:** All cases, users, targets, devices, infrastructure, content, and events in this repository
> are fictional and synthetically generated. This project is not affiliated with or endorsed by OpenAI.
> It contains no real user information and no operationally useful harmful instructions.

## Project Status

**Phase 2 complete — synthetic relational dataset and initial SQL investigation pack**

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
- Initial SQL investigation queries
- Streamlit case explorer
- Documented safety, privacy, and human-review principles

## Investigative Questions

The portfolio is designed to answer questions such as:

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
├── app.py                         # Streamlit portfolio application
├── requirements.txt              # Python dependencies
├── assets/                       # Portfolio images
├── case_briefs/                  # Case reports as they are completed
├── data/                         # Synthetic CSV tables
├── database/                     # SQLite database
├── docs/                         # Methodology, ethics, and governance
├── notebooks/                    # Python analysis notebooks
├── reports/                      # Executive and technical reports
├── scripts/                      # Dataset validation and utilities
└── sql/                          # Investigation queries
```

## Run the Dashboard Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Use the SQLite Database

The database can be opened in DB Browser for SQLite or queried directly:

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

Every case product will distinguish among:

- observed facts
- derived indicators
- analytical judgments
- alternative explanations
- confidence assessments
- recommended actions
- limitations and collection gaps

Automation supports triage and pattern discovery; it does not replace accountable human judgment.

## Planned Deliverables

- [x] Case taxonomy and cross-case pattern library
- [x] Synthetic relational dataset
- [x] Initial SQL investigation pack
- [x] Interactive case explorer
- [ ] Python feature-engineering notebook
- [ ] Cross-case network graph and entity-resolution model
- [ ] Ten investigative case briefs
- [ ] Detection methodology and evaluation report
- [ ] Executive intelligence report
- [ ] Public portfolio website

## Author

**Joel L. Vandenhouten**  
Retired U.S. Army Major | Intelligence, Investigations, Corporate Security, Crisis Operations  
Texas A&M University School of Law — Master of Legal Studies candidate, Cybersecurity Law & Policy

This project is an independent professional portfolio using wholly synthetic data.
