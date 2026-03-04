import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import Contact, Event

DB_PATH = Path.home() / ".my_secretary" / "data.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL CHECK(category IN ('work', 'friend', 'family')),
            company TEXT,
            position TEXT,
            phone TEXT,
            email TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """,
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT,
            occurred_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
        )
    """,
    )

    conn.commit()
    conn.close()


def row_to_contact(row: sqlite3.Row) -> Contact:
    return Contact(
        id=row["id"],
        name=row["name"],
        category=row["category"],
        company=row["company"],
        position=row["position"],
        phone=row["phone"],
        email=row["email"],
        created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
        updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
    )


def row_to_event(row: sqlite3.Row) -> Event:
    return Event(
        id=row["id"],
        contact_id=row["contact_id"],
        type=row["type"],
        subject=row["subject"],
        content=row["content"],
        occurred_at=datetime.fromisoformat(row["occurred_at"]) if row["occurred_at"] else None,
        created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
    )


# Contact operations
def add_contact(contact: Contact) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO contacts (name, category, company, position, phone, email)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (contact.name, contact.category, contact.company, contact.position, contact.phone, contact.email),
    )
    conn.commit()
    contact_id = cursor.lastrowid
    conn.close()
    return contact_id


def get_contact(contact_id: int) -> Optional[Contact]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_contact(row)
    return None


def list_contacts(category: Optional[str] = None) -> list[Contact]:
    conn = get_connection()
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT * FROM contacts WHERE category = ? ORDER BY name", (category,))
    else:
        cursor.execute("SELECT * FROM contacts ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return [row_to_contact(row) for row in rows]


def update_contact(contact_id: int, **kwargs) -> bool:
    allowed = ["name", "category", "company", "position", "phone", "email"]
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    if not updates:
        return False

    updates["updated_at"] = datetime.now().isoformat()
    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = list(updates.values()) + [contact_id]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE contacts SET {set_clause} WHERE id = ?", values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_contact(contact_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


# Event operations
def add_event(event: Event) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO events (contact_id, type, subject, content, occurred_at)
           VALUES (?, ?, ?, ?, ?)""",
        (event.contact_id, event.type, event.subject, event.content, event.occurred_at),
    )
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    return event_id


def get_event(event_id: int) -> Optional[Event]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_event(row)
    return None


def list_events(contact_id: Optional[int] = None, event_type: Optional[str] = None) -> list[Event]:
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if contact_id:
        query += " AND contact_id = ?"
        params.append(contact_id)
    if event_type:
        query += " AND type = ?"
        params.append(event_type)

    query += " ORDER BY occurred_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [row_to_event(row) for row in rows]


def update_event(event_id: int, **kwargs) -> bool:
    allowed = ["contact_id", "type", "subject", "content", "occurred_at"]
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    if not updates:
        return False

    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = list(updates.values()) + [event_id]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE events SET {set_clause} WHERE id = ?", values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_event(event_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def search_events(keyword: str) -> list[Event]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM events WHERE subject LIKE ? OR content LIKE ? ORDER BY occurred_at DESC",
        (f"%{keyword}%", f"%{keyword}%"),
    )
    rows = cursor.fetchall()
    conn.close()
    return [row_to_event(row) for row in rows]


def get_stats() -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM contacts")
    total_contacts = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) FROM contacts GROUP BY category")
    by_category = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT type, COUNT(*) FROM events GROUP BY type")
    by_type = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()

    return {
        "total_contacts": total_contacts,
        "by_category": by_category,
        "total_events": total_events,
        "by_type": by_type,
    }
