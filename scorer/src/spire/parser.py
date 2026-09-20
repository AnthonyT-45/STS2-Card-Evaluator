import json
import logging

logger = logging.getLogger(__name__)


def read_card_choices(run_id, player_id, acts, map_point_history):
    rows = []
    for act_index, act in enumerate(map_point_history):
        act_name = acts[act_index] if act_index < len(acts) else None
        for floor_index, floor in enumerate(act):
            map_point_type = floor["map_point_type"]
            for stats in floor.get("player_stats", []):
                if stats["player_id"] != player_id:
                    continue
                choices = stats.get("card_choices") or []
                option_count = len(choices)
                picked_count = sum(1 for c in choices if c["was_picked"])
                for option_index, choice in enumerate(choices):
                    card = choice["card"]
                    enchantment = card.get("enchantment") or {}
                    rows.append(
                        (
                            run_id,
                            act_index,
                            floor_index,
                            option_index,
                            act_name,
                            map_point_type,
                            option_count,
                            picked_count,
                            card["id"],
                            card.get("current_upgrade_level"),
                            enchantment.get("id"),
                            enchantment.get("amount"),
                            choice["was_picked"],
                        )
                    )
    return rows


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
                start_time = data["start_time"]
                run_time = data["run_time"]
                killed_by_encounter = data["killed_by_encounter"]
                killed_by_event = data["killed_by_event"]
                schema_version = data["schema_version"]

                for player in data["players"]:
                    run_id = f"{file.stem}:{player['id']}"
                    character = player["character"]
                    max_potion_slot_count = player["max_potion_slot_count"]
                    run_row = (
                        run_id,
                        start_time,
                        run_time,
                        character,
                        ascension,
                        is_win,
                        killed_by_encounter,
                        killed_by_event,
                        max_potion_slot_count,
                        seed,
                        schema_version,
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

                    choice_rows = read_card_choices(
                        run_id,
                        player["id"],
                        data["acts"],
                        data["map_point_history"],
                    )

                    yield (run_row, card_rows, relic_rows, potion_rows, choice_rows)

                logger.info(f"Success: read .run file: {file.name}")
            except json.JSONDecodeError:
                logger.error(f"Error: {file.name} is not valid JSON.")
