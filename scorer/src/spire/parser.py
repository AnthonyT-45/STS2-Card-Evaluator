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
                logger.info(f"Success: read .run file: {file.name}")
            except json.JSONDecodeError:
                logger.error(f"Error: {file.name} is not valid JSON.")
