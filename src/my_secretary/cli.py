import typer
from rich.console import Console

from . import db
from .commands.contact import contact_app
from .commands.event import event_app

app = typer.Typer(help="My Secretary - Contact and Event Management System")
console = Console()


@app.callback()
def callback():
    """Initialize database on startup"""
    db.init_db()


app.add_typer(contact_app, name="contact")
app.add_typer(event_app, name="event")


@app.command("stats")
def stats():
    """Show statistics"""
    stats_data = db.get_stats()

    console.print("[bold]Statistics[/bold]")
    console.print("\n[bold cyan]Contacts:[/bold cyan]")
    console.print(f"Total: {stats_data['total_contacts']}")
    if stats_data["by_category"]:
        console.print("By category:")
        for cat, count in stats_data["by_category"].items():
            console.print(f"  - {cat}: {count}")
    else:
        console.print("  No contacts yet")

    console.print("\n[bold cyan]Events:[/bold cyan]")
    console.print(f"Total: {stats_data['total_events']}")
    if stats_data["by_type"]:
        console.print("By type:")
        for typ, count in stats_data["by_type"].items():
            console.print(f"  - {typ}: {count}")
    else:
        console.print("  No events yet")


@app.command()
def search(keyword: str = typer.Argument(..., help="Search keyword")):
    """Search events by keyword"""
    events = db.search_events(keyword)

    if not events:
        console.print("[yellow]No events found matching the keyword[/yellow]")
        return

    console.print(f"[bold]Found {len(events)} event(s):[/bold]\n")

    for e in events:
        contact = db.get_contact(e.contact_id)
        contact_name = contact.name if contact else f"Contact {e.contact_id}"
        console.print(f"[magenta]Event #{e.id}[/magenta] - {e.type}")
        console.print(f"  Contact: {contact_name}")
        console.print(f"  Subject: {e.subject}")
        if e.content:
            console.print(f"  Content: {e.content[:100]}{'...' if len(e.content) > 100 else ''}")
        console.print(f"  Time: {e.occurred_at}")
        console.print()


def main():
    app()
