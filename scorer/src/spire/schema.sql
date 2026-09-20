CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    character TEXT NOT NULL,
    ascension INTEGER NOT NULL,
    is_win INTEGER NOT NULL,
    seed TEXT NOT NULL,
    acts TEXT NOT NULL,
    was_abandoned INTEGER NOT NULL,
    build_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cards (
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    deck_index INTEGER NOT NULL,
    card_id TEXT NOT NULL,
    floor_added_to_deck INTEGER NOT NULL,
    current_upgrade_level INTEGER,
    enchantment_id TEXT,
    enchantment_amount INTEGER,
    PRIMARY KEY (run_id, deck_index)
);

CREATE TABLE IF NOT EXISTS relics (
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    relic_index INTEGER NOT NULL,
    relic_id TEXT NOT NULL,
    floor_added_to_deck INTEGER NOT NULL,
    PRIMARY KEY (run_id, relic_index)
);

CREATE TABLE IF NOT EXISTS potions (
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    potion_index INTEGER NOT NULL,
    potion_id TEXT NOT NULL,
    PRIMARY KEY (run_id, potion_index)
);
