# My Secretary - Claude Code 开发指南

## 项目结构

```
src/my_secretary/
├── __init__.py
├── cli.py           # CLI 入口，使用 typer
├── db.py            # SQLite 数据库操作
├── models.py        # 数据类定义 (Contact, Event)
└── commands/
    ├── contact.py   # 联系人子命令
    └── event.py     # 事件子命令
```

## 技术栈

- **CLI 框架**: typer
- **输出美化**: rich
- **数据库**: SQLite (SQLAlchemy)
- **包管理**: uv

## 开发命令

```bash
# 安装依赖并以可编辑模式安装
make install

# 运行测试
make test

# 运行 CLI
make run
```

## 数据库设计

### contacts 表
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- category (TEXT) - 限制为 work/friend/family
- company, position, phone, email (TEXT, 可选)
- created_at, updated_at (DATETIME)

### events 表
- id (INTEGER PRIMARY KEY)
- contact_id (INTEGER FOREIGN KEY)
- type (TEXT) - 用户自定义类型
- subject (TEXT)
- content (TEXT, 可选)
- occurred_at, created_at (DATETIME)

## 关键模块

- `db.py`: 数据库初始化和 CRUD 操作
- `models.py`: Contact 和 Event 数据类
- `cli.py`: 主 CLI 入口，注册子命令

## 测试

测试文件位于 `tests/test_core.py`，使用 pytest 和临时目录隔离数据库。
