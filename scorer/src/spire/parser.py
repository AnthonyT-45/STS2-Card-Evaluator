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
                    yield (
                        run_id,
                        character,
                        ascension,
                        is_win,
                        seed,
                        acts,
                        was_abandoned,
                        build_id,
                    )

                """
                logger.info(f"ascension: {ascension}")
                logger.info(f"is_win: {is_win}")
                logger.info(f"seed: {seed}")s
                logger.info(f"acts: {acts}")
                logger.info(f"was_abandoned: {was_abandoned}")
                logger.info(f"build_id: {build_id}")s
                """
                logger.info(f"Success: read .run file: {file.name}")
            except json.JSONDecodeError:
                logger.error(f"Error: {file.name} is not valid JSON.")
