"""C-009 synthetic investigation analysis.

This script analyzes wholly synthetic data. It produces investigative leads,
not enforcement conclusions. Human validation is required.
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DB_PATH = BASE / "database" / "openai_abuse_investigator_synthetic.sqlite"
OUTPUT_DIR = BASE / "data"
CASE_ID = "C-009"


def query(connection: sqlite3.Connection, sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, connection)


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as connection:
        cross_case_accounts = query(
            connection,
            """
            SELECT ca.account_id,
                   GROUP_CONCAT(DISTINCT ca.case_id) AS cases,
                   COUNT(DISTINCT ca.case_id) AS case_count,
                   a.role,
                   a.prior_enforcement,
                   a.risk_tier
            FROM case_accounts ca
            JOIN accounts a ON a.account_id = ca.account_id
            WHERE ca.account_id IN (
                SELECT account_id FROM case_accounts WHERE case_id = 'C-009'
            )
            GROUP BY ca.account_id, a.role, a.prior_enforcement, a.risk_tier
            HAVING COUNT(DISTINCT ca.case_id) > 1
            ORDER BY case_count DESC, ca.account_id
            """,
        )

        role_summary = query(
            connection,
            """
            SELECT a.role,
                   COUNT(*) AS event_count,
                   ROUND(AVG(CAST(e.raw_risk_score AS REAL)), 3) AS avg_risk,
                   COUNT(DISTINCT e.account_id) AS account_count
            FROM events e
            JOIN accounts a ON a.account_id = e.account_id
            WHERE e.case_id = 'C-009'
            GROUP BY a.role
            ORDER BY event_count DESC
            """,
        )

        case_links = query(
            connection,
            """
            SELECT CASE
                       WHEN case_id_a = 'C-009' THEN case_id_b
                       ELSE case_id_a
                   END AS linked_case,
                   link_type,
                   CAST(strength AS REAL) AS strength,
                   CAST(evidence_count AS INTEGER) AS evidence_count,
                   analyst_confidence
            FROM case_links
            WHERE case_id_a = 'C-009' OR case_id_b = 'C-009'
            ORDER BY strength DESC
            """,
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cross_case_accounts.to_csv(OUTPUT_DIR / "c009_cross_case_accounts.csv", index=False)
    role_summary.to_csv(OUTPUT_DIR / "c009_role_summary.csv", index=False)
    case_links.to_csv(OUTPUT_DIR / "c009_case_links.csv", index=False)

    print("C-009 analysis complete.")
    print(f"Cross-case accounts: {len(cross_case_accounts)}")
    print(f"Network roles: {len(role_summary)}")
    print(f"Direct linked cases: {len(case_links)}")


if __name__ == "__main__":
    main()
