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
        run_id, start_time, run_time, character, ascension, is_win,
        killed_by_encounter, killed_by_event, max_potion_slot_count,
        seed, schema_version, acts, was_abandoned, build_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
card_choices_insert = """
    INSERT OR REPLACE INTO card_choices (
        run_id, act_index, floor_index, round_num, option_index, act,
        map_point_type, option_count, picked_count, card_id,
        current_upgrade_level, enchantment_id, enchantment_amount, was_picked
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
deck_events_insert = """
    INSERT OR REPLACE INTO deck_events (
        run_id, act_index, floor_index, seq, event_type, card_id,
        related_card_id, enchantment_id, enchantment_amount
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

def connect_db():
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_path.read_text(encoding="utf-8"))
        with conn:
            for run_row, cards, relics, potions, choices, deck_events in parser.read_data(fp):
                conn.execute(runs_insert, run_row)
                conn.executemany(cards_insert, cards)
                conn.executemany(relics_insert, relics)
                conn.executemany(potions_insert, potions)
                conn.executemany(card_choices_insert, choices)
                conn.executemany(deck_events_insert, deck_events)
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
