#!/bin/bash
# My Secretary 数据库维护脚本
# 每次查询前调用，确保数据库已初始化并做备份

DB_PATH="$HOME/.my_secretary/data.db"
BACKUP_DIR="$HOME/.my_secretary/backups"
TODAY=$(date +%Y-%m-%d)

# 创建数据目录和备份目录
mkdir -p "$(dirname "$DB_PATH")"
mkdir -p "$BACKUP_DIR"

# 1. 检查并初始化数据库（如果表不存在）
if [ ! -f "$DB_PATH" ]; then
  echo "数据库不存在，正在初始化..."
  bash "$(dirname "$0")/init_db.sh" "$DB_PATH"
else
  # 检查表是否存在
  TABLE_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('contacts', 'events');")
  if [ "$TABLE_COUNT" -lt 2 ]; then
    echo "数据库表不完整，正在初始化..."
    bash "$(dirname "$0")/init_db.sh" "$DB_PATH"
  fi
fi

# 2. 检查并创建备份（每天第一次查询时）
BACKUP_FILE="$BACKUP_DIR/my-secretary-${TODAY}.db"
if [ ! -f "$BACKUP_FILE" ]; then
  # 检查当天是否已有其他时间的备份
  TODAY_EXISTING=$(ls -1 "$BACKUP_DIR"/my-secretary-*.db 2>/dev/null | grep -c "${TODAY}" || true)
  if [ "$TODAY_EXISTING" -eq 0 ]; then
    echo "创建每日备份: $BACKUP_FILE"
    cp "$DB_PATH" "$BACKUP_FILE"
  fi
fi

# 3. 清理30天前的旧备份
find "$BACKUP_DIR" -name "my-secretary-*.db" -mtime +30 -delete
