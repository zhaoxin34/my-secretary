---
name: my-secretary
description: This skill should be used when the user wants to manage contacts, track events/interactions with contacts, or view contact/event statistics. Useful for adding, listing, updating, deleting contacts and events.
---

# My Secretary - 联系人与事件管理

这是一个 CLI 工具，用于管理联系人和与他们相关的事件交互记录。

## 运行方式

```bash
my-secretary <command>
```

## 联系人管理

```bash
# 添加联系人（姓名唯一，自动加后缀）
my-secretary contact add --name "姓名" --category work --company "公司" --email "邮箱"

# 添加带昵称的联系人（多个昵称用逗号分隔）
my-secretary contact add --name "张三" --nickname "三儿、小张"

# 搜索联系人（同时搜索姓名和昵称）
my-secretary contact list --search "三"

# 按类别筛选
my-secretary contact list --category work

# 查看联系人详情
my-secretary contact get <id>

# 更新联系人
my-secretary contact update <id> --name "新名字"

# 删除联系人
my-secretary contact delete <id>
```

### work 类型特有的字段

```bash
my-secretary contact add --name "张三" --category work \
  --contract-entity "合同主体" \
  --dept-level1 "一级部门" \
  --dept-level2 "二级部门" \
  --entry-date "2024-01-15" \
  --onsite --not-left
```

## 事件管理

```bash
# 添加事件（联系人用姓名，多个用逗号分隔）
my-secretary event add --contacts "张三,王大伟" --type meeting --subject "主题" --content "内容"

# 列出事件
my-secretary event list

# 模糊搜索联系人
my-secretary event list --contact "张三"

# 按类型筛选
my-secretary event list --type email
my-secretary event list --type meeting

# 查看事件详情
my-secretary event get <id>

# 更新事件
my-secretary event update <id> --subject "新主题"

# 删除事件
my-secretary event delete <id>
```

## 其他命令

```bash
# 统计信息
my-secretary stats

# 搜索事件（搜索主题、内容、联系人）
my-secretary search "关键词"
```

## 字段说明

- category: work / friend / family
- nickname: 多个昵称用逗号分隔（如 "三儿、小张"）
- contacts (事件): 多个联系人用逗号分隔（如 "张三,李四"）
- type (事件): email / chat / phone / meeting / 微信 / 钉钉 / 线下 等

## 画像管理

```bash
# 查看画像（通过 ID）
my-secretary profile get <id>

# 按姓名搜索联系人并查看画像
my-secretary profile get-by-name "张三"

# 更新画像
my-secretary profile update <id> --personality "性格描述" --status busy

# 画像标签管理
my-secretary profile tag add <id> --tag "标签名" --type personality
my-secretary profile tag list <id>
my-secretary profile tag delete <id> --tag "标签名"

# 画像关系管理
my-secretary profile relation add <id> --related <相关联系人ID> --type colleague
my-secretary profile relation list <id>
my-secretary profile relation delete <id> --related <相关联系人ID>

# 画像项目管理
my-secretary profile project add <id> --project "项目名"
my-secretary profile project list <id>
my-secretary profile project delete <id> --project "项目名"
```

## 脚本

```bash
# 搜索联系人并查看画像（通过姓名）
.claude/skills/my-secretary/profile_lookup.sh "张三"
```
