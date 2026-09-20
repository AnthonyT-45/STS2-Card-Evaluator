import logging
import sqlite3
from pathlib import Path

from . import parser

logger = logging.getLogger(__name__)

fp = Path(__file__).resolve().parents[2] / "tests" / "fixtures"
db_path = Path(__file__).resolve().parents[2] / "runs.db"
schema_path = Path(__file__).parent / "schema.sql"
runs_insert = """
    INSERT OR REPLACE INTO runs (
        run_id, character, ascension, is_win, seed, acts, was_abandoned, build_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
cards_insert = """
    INSERT OR REPLACE INTO cards (
        run_id, deck_index, card_id, floor_added_to_deck,
        current_upgrade_level, enchantment_id, enchantment_amount
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """
relics_insert = """
    INSERT OR REPLACE INTO relics (
        run_id, relic_index, relic_id, floor_added_to_deck
    ) VALUES (?, ?, ?, ?)
    """
potions_insert = """
    INSERT OR REPLACE INTO potions (
        run_id, potion_index, potion_id
    ) VALUES (?, ?, ?)
    """


def connect_db():
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_path.read_text(encoding="utf-8"))
        with conn:
            for run_row, cards, relics, potions in parser.read_data(fp):
                conn.execute(runs_insert, run_row)
                conn.executemany(cards_insert, cards)
                conn.executemany(relics_insert, relics)
                conn.executemany(potions_insert, potions)
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
