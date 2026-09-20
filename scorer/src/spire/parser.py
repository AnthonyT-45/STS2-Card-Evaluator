import json
import logging

logger = logging.getLogger(__name__)


def read_data(fp):
    if not fp.is_dir():
        raise FileNotFoundError(f"No such directory: {fp}")
    for file in fp.glob("*.run"):
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)

                ascension = data["ascension"]
                is_win = data["win"]
                seed = data["seed"]
                acts = json.dumps(data["acts"])
                was_abandoned = data["was_abandoned"]
                build_id = data["build_id"]

                for player in data["players"]:
                    run_id = f"{file.stem}:{player['id']}"
                    character = player["character"]
                    run_row = (
                        run_id,
                        character,
                        ascension,
                        is_win,
                        seed,
                        acts,
                        was_abandoned,
                        build_id,
                    )
                    card_rows = []
                    for i, card in enumerate(player["deck"]):
                        enchantment = card.get("enchantment") or {}
                        card_rows.append(
                            (
                                run_id,
                                i,
                                card["id"],
                                card["floor_added_to_deck"],
                                card.get("current_upgrade_level"),
                                enchantment.get("id"),
                                enchantment.get("amount"),
                            )
                        )
                    relic_rows = [
                        (run_id, i, relic["id"], relic["floor_added_to_deck"])
                        for i, relic in enumerate(player["relics"])
                    ]

                    potion_rows = [
                        (run_id, potion["slot_index"], potion["id"])
                        for potion in player["potions"]
                    ]

                    yield (run_row, card_rows, relic_rows, potion_rows)

                logger.info(f"Success: read .run file: {file.name}")
            except json.JSONDecodeError:
                logger.error(f"Error: {file.name} is not valid JSON.")
