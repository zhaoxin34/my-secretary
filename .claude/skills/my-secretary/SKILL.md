---
name: my-secretary
description: 个人联系人和事件记录管理。当用户提到联系人、会议、沟通、交流、记录事件、查看联系人的时候使用。或者当用户问某人是个什么样的人时，可以从画像表里查到。通过 sqlite3 直接操作 SQLite 数据库存储联系人和事件信息。
allowed-tools: Bash(bash:*), Bash(sqlite3:*)
---

# My Secretary - 联系人和事件管理

## 脚本路径（重要）

本技能可能通过软链接安装到 `~/.workbuddy/skills/my-secretary` 等位置，工作目录不一定是技能目录。
**必须使用下面的绝对路径调用脚本**，不要用 `./scripts/...` 相对路径：

```bash
SKILL_DIR="/Volumes/data/working/ai/my-secretary/.claude/skills/my-secretary"
```

## 数据库

- 路径：`~/.my_secretary/data.db`（默认，脚本会自动创建）
- 备份目录：`~/.my_secretary/backups`（每日首次调用自动备份，保留 30 天）
- 脚本：`$SKILL_DIR/scripts/init_db.sh`、`$SKILL_DIR/scripts/maintain_db.sh`

## 使用流程

1. **先执行维护脚本**（自动建库、建表、每日备份）：

   ```bash
   bash /Volumes/data/working/ai/my-secretary/.claude/skills/my-secretary/scripts/maintain_db.sh
   ```

2. 执行查询或其他操作（见下方「操作示例」）
3. 如果仍报错（如表结构缺失），运行初始化脚本：

   ```bash
   bash /Volumes/data/working/ai/my-secretary/.claude/skills/my-secretary/scripts/init_db.sh
   ```

## 使用规范

* 在查找联系人、项目、事件等信息时尽量用like查询，精确度没有太高的要求

## 表结构

### contacts（联系人）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| name | TEXT | 姓名，唯一 |
| category | TEXT | work/friend/family |
| company | TEXT | 公司 |
| position | TEXT | 职位 |
| phone | TEXT | 电话 |
| email | TEXT | 邮箱 |
| nickname | TEXT | 昵称，多个用逗号分隔 |
| contract_entity | TEXT | 合同主体 |
| dept_level1 | TEXT | 一级部门 |
| dept_level2 | TEXT | 二级部门 |
| entry_date | TEXT | 入职日期 |
| is_onsite | INTEGER | 1=驻场, 0=非驻场 |
| has_left | INTEGER | 1=已离职, 0=在职 |
| left_date | TEXT | 离职日期 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### events（事件）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| contacts | TEXT | 联系人姓名，多个用逗号分隔 |
| type | TEXT | 类型：email/chat/phone/meeting/微信/钉钉/线下 |
| subject | TEXT | 主题 |
| content | TEXT | 内容 |
| occurred_at | DATETIME | 发生时间 |
| created_at | DATETIME | 创建时间 |

### profiles（画像标签）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| username | TEXT | 联系人姓名 |
| tag_name | TEXT | 标签名（如：性格、工作百分比、项目等） |
| tag_value | TEXT | 标签值 |
| created_at | DATETIME | 创建时间 |

### project_members（项目成员）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| project_name | TEXT | 项目名称 |
| contact_name | TEXT | 联系人姓名 |
| role | TEXT | 在项目中的角色 |
| joined_at | DATETIME | 加入项目时间 |
| created_at | DATETIME | 创建时间 |

## 操作示例

### 查询联系人
```bash
sqlite3 -header -column ~/.my_secretary/data.db "SELECT name, category, company, position FROM contacts;"
```

### 添加联系人
```bash
sqlite3 ~/.my_secretary/data.db "INSERT INTO contacts (name, category, company, position, dept_level1, dept_level2, entry_date, is_onsite) VALUES ('姓名', 'work', '公司', '职位', '部门', '组', '2024-01-01', 1);"
```

### 查询事件
```bash
sqlite3 -header -column ~/.my_secretary/data.db "SELECT occurred_at, contacts, type, subject FROM events ORDER BY occurred_at DESC;"
```

### 查询某人的画像标签
```bash
sqlite3 -header -column ~/.my_secretary/data.db "SELECT tag_name, tag_value, created_at FROM profiles WHERE username='张三';"
```

### 添加画像标签
```bash
sqlite3 ~/.my_secretary/data.db "INSERT INTO profiles (username, tag_name, tag_value) VALUES ('张三', '性格', '暴躁');"
```
