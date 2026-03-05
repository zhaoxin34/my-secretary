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

---

## profiles 表 - 画像表

用于存储每个联系人的详细画像信息。

### 表结构

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| contact_id | INTEGER | 是 | 关联的联系人ID，外键 |
| personality | TEXT | 否 | 性格特点描述 |
| current_status | TEXT | 否 | 当前状态（如：忙碌、自由、休假） |
| status_note | TEXT | 否 | 状态补充说明 |
| projects | TEXT | 否 | 当前项目列表（JSON数组存储） |
| updated_at | DATETIME | 是 | 更新时间 |

### 说明

- 每个联系人只能有一条画像记录（contact_id 唯一）
- 删除联系人时，画像会级联删除

---

## profile_tags 表 - 画像标签表

用于存储联系人的标签（如性格、技能、兴趣等）。

### 表结构

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| profile_id | INTEGER | 是 | 关联的画像ID，外键 |
| tag | TEXT | 是 | 标签内容 |
| tag_type | TEXT | 否 | 标签类型：personality/skill/interest/other |
| created_at | DATETIME | 是 | 创建时间 |

### 说明

- 删除画像时，标签会级联删除

---

## profile_relations 表 - 画像关系表

用于记录联系人之间的关系（如同事、领导、下属、朋友等）。

### 表结构

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| profile_id | INTEGER | 是 | 关联的画像ID，外键 |
| related_contact_id | INTEGER | 是 | 关联的联系人ID，外键 |
| relation_type | TEXT | 否 | 关系类型：colleague/leader/subordinate/friend/other |
| note | TEXT | 否 | 关系备注 |
| created_at | DATETIME | 是 | 创建时间 |

### 说明

- 删除画像时，关系记录会级联删除
