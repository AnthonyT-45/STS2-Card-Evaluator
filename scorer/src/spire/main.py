import logging
import sqlite3
from pathlib import Path

import parser

logger = logging.getLogger(__name__)

fp = Path(__file__).resolve().parents[2] / "tests" / "fixtures"
db_path = Path(__file__).resolve().parents[2] / "runs.db"
schema_path = Path(__file__).parent / "schema.sql"
run_insert = """
    INSERT OR REPLACE INTO runs (
        run_id, character, ascension, is_win, seed, acts, was_abandoned, build_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """


def connect_db():
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_path.read_text(encoding="utf-8"))
        with conn:
            conn.executemany(run_insert, parser.read_data(fp))
    finally:
        conn.close()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    connect_db()


if __name__ == "__main__":
    main()
