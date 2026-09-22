import sqlite3
from pathlib import Path

import pytest

from spire import deckbuilder, parser
from spire.main import load_db

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def conn():
    conn = sqlite3.connect(":memory:")
    load_db(conn, FIXTURES)
    yield conn
    conn.close()


def test_starting_deck_ironclad():
    deck = deckbuilder.starting_deck("CHARACTER.IRONCLAD", 0)
    assert deck.count("CARD.STRIKE_IRONCLAD") == 5
    assert deck.count("CARD.DEFEND_IRONCLAD") == 4
    assert "CARD.BASH" in deck
    assert "CARD.ASCENDERS_BANE" not in deck


def test_starting_deck_adds_ascenders_bane():
    deck = deckbuilder.starting_deck("CHARACTER.IRONCLAD", 5)
    assert "CARD.ASCENDERS_BANE" in deck


def test_split_rounds():
    six = [{"was_picked": False}] * 6
    assert len(parser.split_rounds(six, "monster")) == 2
    assert len(parser.split_rounds(six, "shop")) == 1
    assert parser.split_rounds([], "monster") == []


def test_replay_matches_final_deck(conn):
    run_ids = [r[0] for r in conn.execute("SELECT run_id FROM runs")]
    failed = [rid for rid in run_ids if not deckbuilder.validate(conn, rid)[0]]
    # start strict; loosen to a threshold if a few runs have untracked events
    assert not failed, f"{len(failed)}/{len(run_ids)} runs failed: {failed[:5]}"
