#!/bin/bash
# 用法: ./profile_lookup.sh "张三"
# 功能: 搜索联系人并查看画像信息

NAME="$1"
if [ -z "$NAME" ]; then
    echo "Usage: $0 <name>"
    exit 1
fi

cd "$(dirname "$0")/.." || exit 1

# 1. 搜索联系人
CONTACTS=$(uv run my-secretary contact list --search "$NAME" 2>/dev/null)

if [ -z "$CONTACTS" ]; then
    echo "No contact found matching '$NAME'"
    exit 1
fi

# 提取所有联系人 ID（从表格输出中提取第一列数字）
# 跳过表头，提取 ID
CONTACT_IDS=$(echo "$CONTACTS" | grep -E "^\s*[0-9]" | awk '{print $1}' | head -5)

if [ -z "$CONTACT_IDS" ]; then
    echo "No contact found matching '$NAME'"
    exit 1
fi

echo "========================================="
echo "Found contacts matching '$NAME'"
echo "========================================="

# 2. 遍历搜索结果，获取每个联系人的画像信息
for CONTACT_ID in $CONTACT_IDS; do
    echo ""
    echo "-----------------------------------------"
    uv run my-secretary profile get "$CONTACT_ID"
    echo "-----------------------------------------"
done
