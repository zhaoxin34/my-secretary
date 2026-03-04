# My Secretary

联系人与事件管理系统 - 一个简单的 CLI 工具，用于管理联系人和与他们相关的事件交互记录。

## 功能特性

- 联系人管理：支持 work/friend/family 三种类别
- 昵称支持：支持多个昵称，用逗号分隔
- 姓名唯一：姓名不允许重复，自动加后缀
- 事件记录：记录与联系人的各种交互（邮件、会议、电话等）
- 统计功能：查看联系人和事件的分类统计
- 搜索功能：支持按姓名和昵称搜索

## 安装

```bash
make install
```

或全局安装：

```bash
uv tool install -e .
```

## 快速开始

### 添加联系人

```bash
my-secretary contact add --name "张三" --category work --company "某公司" --email "zhangsan@example.com"
```

### 搜索联系人（支持姓名和昵称）

```bash
my-secretary contact list --search "三"
```

### 列出所有联系人

```bash
my-secretary contact list
```

### 添加事件

```bash
my-secretary event add --contact 1 --type meeting --subject "项目讨论" --content "讨论了项目细节"
```

### 查看统计

```bash
my-secretary stats
```

### 搜索事件

```bash
my-secretary search "项目"
```

## 命令参考

### 联系人命令

| 命令 | 说明 |
|------|------|
| `contact add` | 添加新联系人 |
| `contact list` | 列出联系人 |
| `contact get <id>` | 查看联系人详情 |
| `contact update <id>` | 更新联系人 |
| `contact delete <id>` | 删除联系人 |

### 事件命令

| 命令 | 说明 |
|------|------|
| `event add` | 添加新事件 |
| `event list` | 列出事件 |
| `event get <id>` | 查看事件详情 |
| `event update <id>` | 更新事件 |
| `event delete <id>` | 删除事件 |

### 其他命令

| 命令 | 说明 |
|------|------|
| `stats` | 显示统计信息 |
| `search <keyword>` | 搜索事件 |

## 联系人字段

| 字段 | 说明 |
|------|------|
| name | 姓名（唯一，不允许重复） |
| nickname | 昵称，多个用逗号分隔（如 "三儿、小张"） |
| category | 类别：work/friend/family |
| company | 公司 |
| position | 职位 |
| phone | 电话 |
| email | 邮箱 |

### work 类型特有字段

| 字段 | 说明 |
|------|------|
| contract_entity | 合同主体 |
| dept_level1 | 一级部门 |
| dept_level2 | 二级部门 |
| entry_date | 入职日期 |
| is_onsite | 是否驻场 |
| has_left | 是否离职 |
| left_date | 离职日期 |

## 使用 Makefile

```bash
make install  # 安装依赖
make test     # 运行测试
make run      # 运行 CLI
make help     # 查看帮助
```

## 数据存储

数据存储在 `~/.my_secretary/data.db` (SQLite)
