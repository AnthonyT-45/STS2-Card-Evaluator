CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    start_time INT NOT NULL,
    run_time INT NOT NULL,
    character TEXT NOT NULL,
    ascension INTEGER NOT NULL,
    is_win INTEGER NOT NULL,
    killed_by_encounter TEXT NOT NULL,
    killed_by_event TEXT NOT NULL,
    max_potion_slot_count INT NOT NULL,
    seed TEXT NOT NULL,
    schema_version INT NOT NULL,
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

CREATE TABLE IF NOT EXISTS card_choices (
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    act_index INTEGER NOT NULL,
    floor_index INTEGER NOT NULL,
    round_num INTEGER NOT NULL,
    option_index INTEGER NOT NULL,
    act TEXT,
    map_point_type TEXT NOT NULL,
    option_count INTEGER NOT NULL,
    picked_count INTEGER NOT NULL,
    card_id TEXT NOT NULL,
    current_upgrade_level INTEGER,
    enchantment_id TEXT,
    enchantment_amount INTEGER,
    was_picked INTEGER NOT NULL,
    PRIMARY KEY (run_id, act_index, floor_index, round_num, option_index)
);

CREATE INDEX IF NOT EXISTS idx_card_choices_card_id ON card_choices(card_id);

CREATE TABLE IF NOT EXISTS deck_events (
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    act_index INTEGER NOT NULL,
    floor_index INTEGER NOT NULL,
    seq INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    card_id TEXT NOT NULL,
    related_card_id TEXT,
    enchantment_id TEXT,
    enchantment_amount INTEGER,
    PRIMARY KEY (run_id, act_index, floor_index, seq)
);