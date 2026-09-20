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