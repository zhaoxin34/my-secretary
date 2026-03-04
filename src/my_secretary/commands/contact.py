import typer
from rich.console import Console
from rich.table import Table

from .. import db
from ..models import Contact

contact_app = typer.Typer(help="Manage contacts")
console = Console()


@contact_app.command("add")
def add(
    name: str = typer.Option(..., "--name", help="Contact name"),
    category: str = typer.Option(..., "--category", help="Category: work/friend/family"),
    company: str = typer.Option(None, "--company", help="Company name"),
    position: str = typer.Option(None, "--position", help="Job position"),
    phone: str = typer.Option(None, "--phone", help="Phone number"),
    email: str = typer.Option(None, "--email", help="Email address"),
):
    if category not in ["work", "friend", "family"]:
        console.print("[red]Category must be one of: work, friend, family[/red]")
        raise typer.Exit(1)

    contact = Contact(id=None, name=name, category=category, company=company, position=position, phone=phone, email=email)
    contact_id = db.add_contact(contact)
    console.print(f"[green]Contact added with ID: {contact_id}[/green]")


@contact_app.command("list")
def list_contacts(category: str = typer.Option(None, "--category", help="Filter by category")):
    contacts = db.list_contacts(category)

    if not contacts:
        console.print("[yellow]No contacts found[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Company")
    table.add_column("Phone")
    table.add_column("Email")

    for c in contacts:
        table.add_row(str(c.id), c.name, c.category, c.company or "-", c.phone or "-", c.email or "-")

    console.print(table)


@contact_app.command("get")
def get(contact_id: int = typer.Argument(..., help="Contact ID")):
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    console.print("[bold]Contact Details[/bold]")
    console.print(f"ID: {contact.id}")
    console.print(f"Name: {contact.name}")
    console.print(f"Category: {contact.category}")
    console.print(f"Company: {contact.company or '-'}")
    console.print(f"Position: {contact.position or '-'}")
    console.print(f"Phone: {contact.phone or '-'}")
    console.print(f"Email: {contact.email or '-'}")
    console.print(f"Created: {contact.created_at}")
    console.print(f"Updated: {contact.updated_at}")


@contact_app.command("update")
def update(
    contact_id: int = typer.Argument(..., help="Contact ID"),
    name: str = typer.Option(None, "--name", help="Contact name"),
    category: str = typer.Option(None, "--category", help="Category: work/friend/family"),
    company: str = typer.Option(None, "--company", help="Company name"),
    position: str = typer.Option(None, "--position", help="Job position"),
    phone: str = typer.Option(None, "--phone", help="Phone number"),
    email: str = typer.Option(None, "--email", help="Email address"),
):
    if category and category not in ["work", "friend", "family"]:
        console.print("[red]Category must be one of: work, friend, family[/red]")
        raise typer.Exit(1)

    updated = db.update_contact(contact_id, name=name, category=category, company=company, position=position, phone=phone, email=email)

    if updated:
        console.print(f"[green]Contact {contact_id} updated[/green]")
    else:
        console.print("[red]Contact not found or no changes made[/red]")
        raise typer.Exit(1)


@contact_app.command("delete")
def delete(contact_id: int = typer.Argument(..., help="Contact ID")):
    deleted = db.delete_contact(contact_id)
    if deleted:
        console.print(f"[green]Contact {contact_id} deleted[/green]")
    else:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)
