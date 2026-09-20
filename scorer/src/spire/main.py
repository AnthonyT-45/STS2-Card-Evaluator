import logging
from pathlib import Path

import parser

fp = Path(__file__).resolve().parents[2] / "tests" / "fixtures"

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    parser.read_data(fp)


if __name__ == "__main__":
    main()
