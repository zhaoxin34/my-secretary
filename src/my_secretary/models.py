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
