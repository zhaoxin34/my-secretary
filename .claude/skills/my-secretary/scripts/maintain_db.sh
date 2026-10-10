#!/bin/bash
# My Secretary 数据库维护脚本
# 每次查询前调用，确保数据库已初始化并做备份
# 用法: bash /path/to/scripts/maintain_db.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="$HOME/.my_secretary/data.db"
BACKUP_DIR="$HOME/.my_secretary/backups"
TODAY=$(date +%Y-%m-%d)

# 依赖检查
if ! command -v sqlite3 >/dev/null 2>&1; then
  echo "错误: 未找到 sqlite3 命令，请先安装 sqlite3" >&2
  exit 1
fi

# 创建数据目录和备份目录
mkdir -p "$(dirname "$DB_PATH")"
mkdir -p "$BACKUP_DIR"

# 1. 检查并初始化数据库（如果表不存在）
if [ ! -f "$DB_PATH" ]; then
  echo "数据库不存在，正在初始化..."
  bash "$SCRIPT_DIR/init_db.sh" "$DB_PATH" || exit 1
else
  # 检查 4 张表是否齐全
  TABLE_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('contacts', 'events', 'profiles', 'project_members');")
  if [ "${TABLE_COUNT:-0}" -lt 4 ]; then
    echo "数据库表不完整（当前 ${TABLE_COUNT:-0}/4），正在初始化..."
    bash "$SCRIPT_DIR/init_db.sh" "$DB_PATH" || exit 1
  fi
fi

# 2. 检查并创建备份（每天第一次查询时）
BACKUP_FILE="$BACKUP_DIR/my-secretary-${TODAY}.db"
if [ ! -f "$BACKUP_FILE" ] && [ -f "$DB_PATH" ]; then
  echo "创建每日备份: $BACKUP_FILE"
  cp "$DB_PATH" "$BACKUP_FILE"
fi

# 3. 清理30天前的旧备份（仅限本技能备份目录下的 my-secretary-*.db）
if [ -d "$BACKUP_DIR" ]; then
  find "$BACKUP_DIR" -maxdepth 1 -type f -name "my-secretary-*.db" -mtime +30 -delete
fi

echo "数据库就绪: $DB_PATH"
