"""Integrity checks for the synthetic investigation dataset."""
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "openai_abuse_investigator_synthetic.sqlite"


def connect() -> sqlite3.Connection:
    assert DB.exists(), f"missing database: {DB}"
    return sqlite3.connect(DB)


def test_expected_counts() -> None:
    con = connect()
    assert con.execute("SELECT COUNT(*) FROM cases").fetchone()[0] == 10
    assert con.execute("SELECT COUNT(*) FROM accounts").fetchone()[0] == 158
    assert con.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 3010
    assert con.execute("SELECT COUNT(*) FROM content").fetchone()[0] == 1989
    assert con.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] == 533
    assert con.execute("SELECT COUNT(*) FROM reports_enforcement").fetchone()[0] == 51
    assert con.execute("SELECT COUNT(*) FROM case_links").fetchone()[0] == 15
    assert con.execute("SELECT COUNT(*) FROM account_links").fetchone()[0] == 136


def test_cases_have_confidence_and_label() -> None:
    con = connect()
    missing = con.execute(
        """
        SELECT COUNT(*) FROM cases
        WHERE ground_truth_label IS NULL OR TRIM(ground_truth_label) = ''
           OR analyst_confidence IS NULL
        """
    ).fetchone()[0]
    assert missing == 0


def test_c009_present() -> None:
    con = connect()
    row = con.execute("SELECT case_id FROM cases WHERE case_id = 'C-009'").fetchone()
    assert row is not None
