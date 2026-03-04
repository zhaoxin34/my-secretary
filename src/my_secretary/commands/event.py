from datetime import datetime
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .. import db
from ..models import Event

event_app = typer.Typer(help="Manage events")
console = Console()


@event_app.command("add")
def add(
    contact: int = typer.Option(..., "--contact", help="Contact ID"),
    type: str = typer.Option(..., "--type", help="Event type (email/chat/phone/meeting/微信/钉钉/线下等)"),
    subject: str = typer.Option(..., "--subject", help="Event subject"),
    content: str = typer.Option(None, "--content", help="Event content summary"),
    occurred_at: str = typer.Option(None, "--occurred-at", help="Occurrence time (ISO format)"),
):
    # Verify contact exists
    contact_obj = db.get_contact(contact)
    if not contact_obj:
        console.print(f"[red]Contact with ID {contact} not found[/red]")
        raise typer.Exit(1)

    occurred = None
    if occurred_at:
        try:
            occurred = datetime.fromisoformat(occurred_at)
        except ValueError:
            console.print("[red]Invalid date format. Use ISO format (e.g., 2024-01-15 14:30:00)[/red]")
            raise typer.Exit(1)
    else:
        occurred = datetime.now()

    event = Event(id=None, contact_id=contact, type=type, subject=subject, content=content, occurred_at=occurred)
    event_id = db.add_event(event)
    console.print(f"[green]Event added with ID: {event_id}[/green]")


@event_app.command("list")
def list_events(
    contact: Optional[int] = typer.Option(None, "--contact", help="Filter by contact ID"),
    type: Optional[str] = typer.Option(None, "--type", help="Filter by event type"),
):
    events = db.list_events(contact_id=contact, event_type=type)

    if not events:
        console.print("[yellow]No events found[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Contact ID")
    table.add_column("Type")
    table.add_column("Subject")
    table.add_column("Occurred At")

    for e in events:
        table.add_row(
            str(e.id),
            str(e.contact_id),
            e.type,
            e.subject[:30] + "..." if len(e.subject) > 30 else e.subject,
            e.occurred_at.strftime("%Y-%m-%d %H:%M") if e.occurred_at else "-",
        )

    console.print(table)


@event_app.command("get")
def get(event_id: int = typer.Argument(..., help="Event ID")):
    event = db.get_event(event_id)
    if not event:
        console.print("[red]Event not found[/red]")
        raise typer.Exit(1)

    contact = db.get_contact(event.contact_id)

    console.print("[bold]Event Details[/bold]")
    console.print(f"ID: {event.id}")
    console.print(f"Contact: {contact.name if contact else event.contact_id}")
    console.print(f"Type: {event.type}")
    console.print(f"Subject: {event.subject}")
    console.print(f"Content: {event.content or '-'}")
    console.print(f"Occurred At: {event.occurred_at}")
    console.print(f"Created: {event.created_at}")


@event_app.command("update")
def update(
    event_id: int = typer.Argument(..., help="Event ID"),
    contact: Optional[int] = typer.Option(None, "--contact", help="Contact ID"),
    type: Optional[str] = typer.Option(None, "--type", help="Event type"),
    subject: Optional[str] = typer.Option(None, "--subject", help="Event subject"),
    content: Optional[str] = typer.Option(None, "--content", help="Event content"),
    occurred_at: Optional[str] = typer.Option(None, "--occurred-at", help="Occurrence time"),
):
    occurred = None
    if occurred_at:
        try:
            occurred = datetime.fromisoformat(occurred_at)
        except ValueError:
            console.print("[red]Invalid date format. Use ISO format[/red]")
            raise typer.Exit(1)

    updated = db.update_event(event_id, contact_id=contact, type=type, subject=subject, content=content, occurred_at=occurred)

    if updated:
        console.print(f"[green]Event {event_id} updated[/green]")
    else:
        console.print("[red]Event not found or no changes made[/red]")
        raise typer.Exit(1)


@event_app.command("delete")
def delete(event_id: int = typer.Argument(..., help="Event ID")):
    deleted = db.delete_event(event_id)
    if deleted:
        console.print(f"[green]Event {event_id} deleted[/green]")
    else:
        console.print("[red]Event not found[/red]")
        raise typer.Exit(1)
