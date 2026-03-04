from datetime import datetime
from typing import Optional

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
    nickname: str = typer.Option(None, "--nickname", help="Nickname(s), comma separated (e.g., '三儿、小张')"),
    # Work-specific fields
    contract_entity: str = typer.Option(None, "--contract-entity", help="Contract entity (合同主体)"),
    dept_level1: str = typer.Option(None, "--dept-level1", help="Level 1 department (一级部门)"),
    dept_level2: str = typer.Option(None, "--dept-level2", help="Level 2 department (二级部门)"),
    entry_date: str = typer.Option(None, "--entry-date", help="Entry date (YYYY-MM-DD)"),
    is_onsite: bool = typer.Option(None, "--onsite/--not-onsite", help="Is on-site (是否驻场)"),
    has_left: bool = typer.Option(None, "--left/--not-left", help="Has left (是否离职)"),
    left_date: str = typer.Option(None, "--left-date", help="Left date (YYYY-MM-DD)"),
):
    if category not in ["work", "friend", "family"]:
        console.print("[red]Category must be one of: work, friend, family[/red]")
        raise typer.Exit(1)

    entry_dt = None
    if entry_date:
        try:
            entry_dt = datetime.strptime(entry_date, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Invalid entry date format. Use YYYY-MM-DD[/red]")
            raise typer.Exit(1)

    left_dt = None
    if left_date:
        try:
            left_dt = datetime.strptime(left_date, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Invalid left date format. Use YYYY-MM-DD[/red]")
            raise typer.Exit(1)

    contact = Contact(
        id=None,
        name=name,
        category=category,
        company=company,
        position=position,
        phone=phone,
        email=email,
        nickname=nickname,
        contract_entity=contract_entity,
        dept_level1=dept_level1,
        dept_level2=dept_level2,
        entry_date=entry_dt,
        is_onsite=is_onsite,
        has_left=has_left,
        left_date=left_dt,
    )
    contact_id = db.add_contact(contact)
    console.print(f"[green]Contact added with ID: {contact_id}[/green]")


@contact_app.command("list")
def list_contacts(
    category: Optional[str] = typer.Option(None, "--category", help="Filter by category"),
    search: Optional[str] = typer.Option(None, "--search", help="Search in name and nickname"),
):
    contacts = db.list_contacts(category=category, search=search)

    if not contacts:
        console.print("[yellow]No contacts found[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Nickname")
    table.add_column("Category")
    table.add_column("Company")
    table.add_column("Phone")
    table.add_column("Email")

    for c in contacts:
        table.add_row(
            str(c.id),
            c.name,
            c.nickname or "-",
            c.category,
            c.company or "-",
            c.phone or "-",
            c.email or "-",
        )

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
    console.print(f"Nickname: {contact.nickname or '-'}")
    console.print(f"Category: {contact.category}")
    console.print(f"Company: {contact.company or '-'}")
    console.print(f"Position: {contact.position or '-'}")
    console.print(f"Phone: {contact.phone or '-'}")
    console.print(f"Email: {contact.email or '-'}")
    console.print("--- Work Info ---")
    console.print(f"Contract Entity: {contact.contract_entity or '-'}")
    console.print(f"Level 1 Dept: {contact.dept_level1 or '-'}")
    console.print(f"Level 2 Dept: {contact.dept_level2 or '-'}")
    console.print(f"Entry Date: {contact.entry_date.strftime('%Y-%m-%d') if contact.entry_date else '-'}")
    console.print(f"Is On-site: {'Yes' if contact.is_onsite else 'No' if contact.is_onsite is not None else '-'}")
    console.print(f"Has Left: {'Yes' if contact.has_left else 'No' if contact.has_left is not None else '-'}")
    console.print(f"Left Date: {contact.left_date.strftime('%Y-%m-%d') if contact.left_date else '-'}")
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
    nickname: str = typer.Option(None, "--nickname", help="Nickname(s), comma separated"),
    contract_entity: str = typer.Option(None, "--contract-entity", help="Contract entity (合同主体)"),
    dept_level1: str = typer.Option(None, "--dept-level1", help="Level 1 department (一级部门)"),
    dept_level2: str = typer.Option(None, "--dept-level2", help="Level 2 department (二级部门)"),
    entry_date: str = typer.Option(None, "--entry-date", help="Entry date (YYYY-MM-DD)"),
    is_onsite: bool = typer.Option(None, "--onsite/--not-onsite", help="Is on-site (是否驻场)"),
    has_left: bool = typer.Option(None, "--left/--not-left", help="Has left (是否离职)"),
    left_date: str = typer.Option(None, "--left-date", help="Left date (YYYY-MM-DD)"),
):
    if category and category not in ["work", "friend", "family"]:
        console.print("[red]Category must be one of: work, friend, family[/red]")
        raise typer.Exit(1)

    entry_dt = None
    if entry_date:
        try:
            entry_dt = datetime.strptime(entry_date, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Invalid entry date format. Use YYYY-MM-DD[/red]")
            raise typer.Exit(1)

    left_dt = None
    if left_date:
        try:
            left_dt = datetime.strptime(left_date, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Invalid left date format. Use YYYY-MM-DD[/red]")
            raise typer.Exit(1)

    updated = db.update_contact(
        contact_id,
        name=name,
        category=category,
        company=company,
        position=position,
        phone=phone,
        email=email,
        nickname=nickname,
        contract_entity=contract_entity,
        dept_level1=dept_level1,
        dept_level2=dept_level2,
        entry_date=entry_dt,
        is_onsite=is_onsite,
        has_left=has_left,
        left_date=left_dt,
    )

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
