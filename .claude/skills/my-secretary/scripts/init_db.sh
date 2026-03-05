#!/bin/bash
# My Secretary 数据库初始化脚本

DB_PATH="${1:-./data/my-secretary.db}"

# 创建数据目录
mkdir -p "$(dirname "$DB_PATH")"

# 初始化数据库和表
sqlite3 "$DB_PATH" <<EOF
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL CHECK(category IN ('work', 'friend', 'family')),
    company TEXT,
    position TEXT,
    phone TEXT,
    email TEXT,
    nickname TEXT,
    contract_entity TEXT,
    dept_level1 TEXT,
    dept_level2 TEXT,
    entry_date TEXT,
    is_onsite INTEGER DEFAULT 0,
    has_left INTEGER DEFAULT 0,
    left_date TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contacts TEXT NOT NULL,
    type TEXT NOT NULL,
    subject TEXT NOT NULL,
    content TEXT,
    occurred_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name);
CREATE INDEX IF NOT EXISTS idx_contacts_category ON contacts(category);
CREATE INDEX IF NOT EXISTS idx_events_contacts ON events(contacts);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(type);
CREATE INDEX IF NOT EXISTS idx_events_occurred_at ON events(occurred_at);
EOF

echo "数据库初始化完成: $DB_PATH"
