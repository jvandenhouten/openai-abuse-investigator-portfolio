from __future__ import annotations

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "openai_abuse_investigator_synthetic.sqlite"


def scalar(connection: sqlite3.Connection, query: str) -> int:
    return int(connection.execute(query).fetchone()[0])


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as connection:
        checks = {
            "cases": scalar(connection, "SELECT COUNT(*) FROM cases"),
            "accounts": scalar(connection, "SELECT COUNT(*) FROM accounts"),
            "events": scalar(connection, "SELECT COUNT(*) FROM events"),
            "case_links": scalar(connection, "SELECT COUNT(*) FROM case_links"),
            "cross_case_accounts": scalar(
                connection,
                """
                SELECT COUNT(*) FROM (
                    SELECT account_id
                    FROM case_accounts
                    GROUP BY account_id
                    HAVING COUNT(DISTINCT case_id) > 1
                )
                """,
            ),
            "shared_cross_case_devices": scalar(
                connection,
                """
                SELECT COUNT(*) FROM (
                    SELECT s.device_id
                    FROM sessions s
                    JOIN events e ON e.session_id=s.session_id
                    GROUP BY s.device_id
                    HAVING COUNT(DISTINCT e.case_id) > 1
                )
                """,
            ),
        }

    expected_minimums = {
        "cases": 10,
        "accounts": 150,
        "events": 3000,
        "case_links": 15,
        "cross_case_accounts": 5,
        "shared_cross_case_devices": 5,
    }

    failed = []
    for name, result in checks.items():
        target = expected_minimums[name]
        status = "PASS" if result >= target else "FAIL"
        print(f"{status:4} | {name:28} | result={result:5} | minimum={target:5}")
        if result < target:
            failed.append(name)

    if failed:
        raise SystemExit(f"Validation failed: {', '.join(failed)}")

    print("\nAll synthetic-dataset integrity checks passed.")


if __name__ == "__main__":
    main()
