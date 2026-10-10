#!/bin/bash
# My Secretary 数据库初始化脚本
# 用法: bash /path/to/scripts/init_db.sh [DB_PATH]
# 不传参数时默认使用 $HOME/.my_secretary/data.db

DB_PATH="${1:-$HOME/.my_secretary/data.db}"

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

CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    tag_name TEXT NOT NULL,
    tag_value TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    role TEXT,
    joined_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name);
CREATE INDEX IF NOT EXISTS idx_contacts_category ON contacts(category);
CREATE INDEX IF NOT EXISTS idx_events_contacts ON events(contacts);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(type);
CREATE INDEX IF NOT EXISTS idx_events_occurred_at ON events(occurred_at);
CREATE INDEX IF NOT EXISTS idx_profiles_username ON profiles(username);
CREATE INDEX IF NOT EXISTS idx_project_members_project ON project_members(project_name);
EOF

echo "数据库初始化完成: $DB_PATH"
