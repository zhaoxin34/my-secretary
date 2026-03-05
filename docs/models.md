# 数据模型

## contacts 表 - 联系人表

用于存储联系人的基本信息。

### 表结构

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| name | TEXT | 是 | 联系人姓名，唯一 |
| category | TEXT | 是 | 类别，枚举值：work/friend/family |
| company | TEXT | 否 | 公司 |
| position | TEXT | 否 | 职位 |
| phone | TEXT | 否 | 电话 |
| email | TEXT | 否 | 邮箱 |
| nickname | TEXT | 否 | 昵称，多个用逗号分隔（如"三儿、小张"） |
| contract_entity | TEXT | 否 | 合同主体 |
| dept_level1 | TEXT | 否 | 一级部门 |
| dept_level2 | TEXT | 否 | 二级部门 |
| entry_date | TEXT | 否 | 入职日期（ISO格式） |
| is_onsite | INTEGER | 否 | 是否驻场（0/1） |
| has_left | INTEGER | 否 | 是否离职（0/1） |
| left_date | TEXT | 否 | 离职日期（ISO格式） |
| created_at | DATETIME | 是 | 创建时间 |
| updated_at | DATETIME | 是 | 更新时间 |

### 索引

- 主键索引：id
- 唯一索引：name（当无重复姓名时创建）

---

## events 表 - 事件表

用于记录与联系人的互动事件。

### 表结构

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| contacts | TEXT | 是 | 联系人姓名，多个用逗号分隔 |
| type | TEXT | 是 | 事件类型，如：email/chat/phone/meeting/微信/钉钉/线下等 |
| subject | TEXT | 是 | 事件主题 |
| content | TEXT | 否 | 事件详细内容 |
| occurred_at | DATETIME | 否 | 事件发生时间 |
| created_at | DATETIME | 是 | 创建时间 |

### 说明

- contacts 字段可以存储多个联系人，用逗号分隔
- 支持按联系人姓名模糊搜索事件
- 支持按事件类型过滤
- 按发生时间倒序排列
