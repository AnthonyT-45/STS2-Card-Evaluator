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
