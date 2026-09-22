from collections import Counter

STARTING_DECKS = {
    "CHARACTER.IRONCLAD": ["CARD.BASH"],
    "CHARACTER.SILENT": ["CARD.SURVIVOR", "CARD.NEUTRALIZE"],
    "CHARACTER.DEFECT": ["CARD.ZAP", "CARD.DUALCAST"],
    "CHARACTER.NECROBINDER": ["CARD.UNLEASH", "CARD.BODYGUARD"],
    "CHARACTER.REGENT": ["CARD.VENERATE", "CARD.FALLING_STAR"],
}
STRIKE_DEFEND_COUNTS = {
    "CHARACTER.IRONCLAD": (5, 4),
    "CHARACTER.SILENT": (5, 5),
    "CHARACTER.DEFECT": (4, 4),
    "CHARACTER.NECROBINDER": (4, 4),
    "CHARACTER.REGENT": (4, 4),
}
ASCENSION_ASCENDERS_BANE = 5
CARD_REMOVING = {"remove", "transform"}


def starting_deck(character, ascension):
    strikes, defends = STRIKE_DEFEND_COUNTS[character]
    character_name = character.removeprefix("CHARACTER.")
    deck = [f"CARD.STRIKE_{character_name}"] * strikes + [
        f"CARD.DEFEND_{character_name}"
    ] * defends
    deck.extend(STARTING_DECKS[character])
    if ascension >= ASCENSION_ASCENDERS_BANE:
        deck.append("CARD.ASCENDERS_BANE")

    return deck


def load_events(conn, run_id):
    return conn.execute(
        """
        SELECT act_index, floor_index, event_type, card_id, related_card_id
        FROM deck_events
        WHERE run_id = ?
        ORDER BY act_index, floor_index, seq
        """,
        (run_id,),
    ).fetchall()


def decks_by_floor(conn, run_id):
    character, ascension = conn.execute(
        "SELECT character, ascension FROM runs WHERE run_id = ?", (run_id,)
    ).fetchone()

    deck = Counter(starting_deck(character, ascension))
    snapshots = {}
    missing = []
    pending = []

    def retry_pending():
        for floor, event_type, card_id in pending:
            if deck[card_id] > 0:
                deck[card_id] -= 1
            else:
                missing.append((floor, event_type, card_id))
        pending.clear()

    for act_index, floor_index, event_type, card_id, related in load_events(
        conn, run_id
    ):
        floor = (act_index, floor_index)
        if floor not in snapshots:
            retry_pending()
            snapshots[floor] = deck.copy()

        if event_type in CARD_REMOVING:
            if deck[card_id] > 0:
                deck[card_id] -= 1
            else:
                pending.append((floor, event_type, card_id))

        if event_type == "transform":
            deck[related] += 1
        elif event_type == "gain":
            deck[card_id] += 1

    retry_pending()
    return snapshots, +deck, missing


def validate(conn, run_id):
    _, replayed, missing = decks_by_floor(conn, run_id)
    actual = Counter(
        card_id
        for (card_id,) in conn.execute(
            "SELECT card_id FROM cards WHERE run_id = ?", (run_id,)
        )
    )
    ok = replayed == actual
    extra = replayed - actual
    lacking = actual - replayed
    return ok, extra, lacking, missing
