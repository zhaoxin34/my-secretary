import pytest
from datetime import datetime

from my_secretary.models import Contact, Event
from my_secretary import db


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Create a temporary database for testing"""
    # Override DB_PATH to use temp directory
    test_db_path = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_PATH", test_db_path)
    db.init_db()
    yield


def test_add_contact(test_db):
    contact = Contact(id=None, name="Test User", category="work", company="Test Corp", email="test@example.com")
    contact_id = db.add_contact(contact)
    assert contact_id == 1

    retrieved = db.get_contact(contact_id)
    assert retrieved is not None
    assert retrieved.name == "Test User"
    assert retrieved.category == "work"


def test_list_contacts(test_db):
    contacts = [
        Contact(id=None, name="User1", category="work"),
        Contact(id=None, name="User2", category="friend"),
        Contact(id=None, name="User3", category="work"),
    ]
    for c in contacts:
        db.add_contact(c)

    all_contacts = db.list_contacts()
    assert len(all_contacts) == 3

    work_contacts = db.list_contacts(category="work")
    assert len(work_contacts) == 2


def test_update_contact(test_db):
    contact = Contact(id=None, name="Original", category="work")
    contact_id = db.add_contact(contact)

    updated = db.update_contact(contact_id, name="Updated", company="New Corp")
    assert updated is True

    retrieved = db.get_contact(contact_id)
    assert retrieved.name == "Updated"
    assert retrieved.company == "New Corp"


def test_delete_contact(test_db):
    contact = Contact(id=None, name="To Delete", category="work")
    contact_id = db.add_contact(contact)

    deleted = db.delete_contact(contact_id)
    assert deleted is True

    retrieved = db.get_contact(contact_id)
    assert retrieved is None


def test_add_event(test_db):
    # First add a contact
    contact = Contact(id=None, name="Event User", category="work")
    contact_id = db.add_contact(contact)

    # Then add an event
    event = Event(
        id=None,
        contact_id=contact_id,
        type="meeting",
        subject="Test Meeting",
        content="Test content",
        occurred_at=datetime.now(),
    )
    event_id = db.add_event(event)
    assert event_id == 1

    retrieved = db.get_event(event_id)
    assert retrieved is not None
    assert retrieved.subject == "Test Meeting"


def test_list_events(test_db):
    # Add contacts and events
    c1 = Contact(id=None, name="User1", category="work")
    c2 = Contact(id=None, name="User2", category="friend")
    c1_id = db.add_contact(c1)
    c2_id = db.add_contact(c2)

    events = [
        Event(id=None, contact_id=c1_id, type="email", subject="Email 1"),
        Event(id=None, contact_id=c1_id, type="meeting", subject="Meeting 1"),
        Event(id=None, contact_id=c2_id, type="chat", subject="Chat 1"),
    ]
    for e in events:
        db.add_event(e)

    all_events = db.list_events()
    assert len(all_events) == 3

    user1_events = db.list_events(contact_id=c1_id)
    assert len(user1_events) == 2

    email_events = db.list_events(event_type="email")
    assert len(email_events) == 1


def test_search_events(test_db):
    contact = Contact(id=None, name="Search User", category="work")
    contact_id = db.add_contact(contact)

    events = [
        Event(id=None, contact_id=contact_id, type="email", subject="Project Update", content="About project"),
        Event(id=None, contact_id=contact_id, type="meeting", subject="Other Meeting", content="Random"),
    ]
    for e in events:
        db.add_event(e)

    results = db.search_events("project")
    assert len(results) == 1
    assert results[0].subject == "Project Update"


def test_stats(test_db):
    # Add test data
    contacts = [
        Contact(id=None, name="Work1", category="work"),
        Contact(id=None, name="Work2", category="work"),
        Contact(id=None, name="Friend1", category="friend"),
    ]
    for c in contacts:
        db.add_contact(c)

    c1_id = db.get_contact(1).id
    events = [
        Event(id=None, contact_id=c1_id, type="email", subject="Email 1"),
        Event(id=None, contact_id=c1_id, type="meeting", subject="Meeting 1"),
    ]
    for e in events:
        db.add_event(e)

    stats = db.get_stats()
    assert stats["total_contacts"] == 3
    assert stats["by_category"]["work"] == 2
    assert stats["by_category"]["friend"] == 1
    assert stats["total_events"] == 2
