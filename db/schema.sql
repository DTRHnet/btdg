-- BTDigg Clone Database Schema
-- SQLite database for storing torrent information

-- Main torrents table
CREATE TABLE IF NOT EXISTS torrents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    info_hash TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    size INTEGER NOT NULL DEFAULT 0,
    files INTEGER NOT NULL DEFAULT 0,
    added INTEGER NOT NULL,
    seeds INTEGER NOT NULL DEFAULT 0,
    peers INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    magnet_link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better search performance
CREATE INDEX IF NOT EXISTS idx_torrents_info_hash ON torrents(info_hash);
CREATE INDEX IF NOT EXISTS idx_torrents_title ON torrents(title);
CREATE INDEX IF NOT EXISTS idx_torrents_added ON torrents(added);
CREATE INDEX IF NOT EXISTS idx_torrents_size ON torrents(size);
CREATE INDEX IF NOT EXISTS idx_torrents_seeds ON torrents(seeds);

-- Full-text search index
CREATE VIRTUAL TABLE IF NOT EXISTS torrents_fts USING fts5(
    title,
    description,
    content='torrents',
    content_rowid='id'
);

-- Triggers to keep FTS index in sync
CREATE TRIGGER IF NOT EXISTS torrents_ai AFTER INSERT ON torrents BEGIN
    INSERT INTO torrents_fts(rowid, title, description) VALUES (new.id, new.title, new.description);
END;

CREATE TRIGGER IF NOT EXISTS torrents_ad AFTER DELETE ON torrents BEGIN
    INSERT INTO torrents_fts(torrents_fts, rowid, title, description) VALUES('delete', old.id, old.title, old.description);
END;

CREATE TRIGGER IF NOT EXISTS torrents_au AFTER UPDATE ON torrents BEGIN
    INSERT INTO torrents_fts(torrents_fts, rowid, title, description) VALUES('delete', old.id, old.title, old.description);
    INSERT INTO torrents_fts(rowid, title, description) VALUES (new.id, new.title, new.description);
END;

-- Statistics table
CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_torrents INTEGER NOT NULL DEFAULT 0,
    total_size INTEGER NOT NULL DEFAULT 0,
    total_files INTEGER NOT NULL DEFAULT 0,
    active_seeds INTEGER NOT NULL DEFAULT 0,
    active_peers INTEGER NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search history table (for analytics)
CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    results_count INTEGER NOT NULL DEFAULT 0,
    search_time REAL NOT NULL DEFAULT 0,
    user_agent TEXT,
    ip_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for search history
CREATE INDEX IF NOT EXISTS idx_search_history_query ON search_history(query);
CREATE INDEX IF NOT EXISTS idx_search_history_created_at ON search_history(created_at);

-- Insert initial statistics record
INSERT OR IGNORE INTO statistics (id, total_torrents, total_size, total_files, active_seeds, active_peers) 
VALUES (1, 0, 0, 0, 0, 0);
