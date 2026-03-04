from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Contact:
    id: Optional[int]
    name: str
    category: str  # work/friend/family
    company: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: Optional[str] = None  # 昵称，多个用逗号分隔，如 "三儿、小张"
    # Work-specific fields
    contract_entity: Optional[str] = None  # 合同主体
    dept_level1: Optional[str] = None  # 一级部门
    dept_level2: Optional[str] = None  # 二级部门
    entry_date: Optional[datetime] = None  # 入职日期
    is_onsite: Optional[bool] = None  # 是否驻场
    has_left: Optional[bool] = None  # 是否离职
    left_date: Optional[datetime] = None  # 已离职日期
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Event:
    id: Optional[int]
    contact_id: int
    type: str  # email/chat/phone/meeting/微信/钉钉/线下等
    subject: str
    content: Optional[str] = None
    occurred_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
