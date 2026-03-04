import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .. import db

profile_app = typer.Typer(help="Manage contact profiles")
console = Console()


def get_contact_name(contact_id: int) -> str:
    """Helper to get contact name by ID"""
    contact = db.get_contact(contact_id)
    return contact.name if contact else f"Unknown (ID: {contact_id})"


@profile_app.command("get")
def get(contact_id: int = typer.Argument(..., help="Contact ID")):
    """View contact profile"""
    # Check if contact exists
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    profile = db.get_profile(contact_id)

    console.print(f"\n[bold cyan]Contact Profile: {contact.name}[/bold cyan]")
    console.print(f"ID: {contact_id}")
    console.print(f"Category: {contact.category}")
    console.print(f"Company: {contact.company or '-'}")
    console.print(f"Position: {contact.position or '-'}")

    if not profile:
        console.print("\n[yellow]No profile yet. Use 'profile update' to create one.[/yellow]")
        return

    console.print("\n[bold]--- Profile ---[/bold]")
    console.print(f"Personality: {profile.personality or '-'}")
    console.print(f"Current Status: {profile.current_status or '-'}")
    console.print(f"Status Note: {profile.status_note or '-'}")

    # Projects
    if profile.projects:
        try:
            projects = json.loads(profile.projects)
            if projects:
                console.print("Projects:")
                for p in projects:
                    console.print(f"  - {p}")
        except json.JSONDecodeError:
            console.print(f"Projects: {profile.projects}")
    else:
        console.print("Projects: -")

    # Tags
    tags = db.get_profile_tags(profile.id)
    if tags:
        console.print("\n[bold]--- Tags ---[/bold]")
        by_type = {}
        for tag in tags:
            if tag.tag_type not in by_type:
                by_type[tag.tag_type] = []
            by_type[tag.tag_type].append(tag.tag)

        for tag_type, tag_list in by_type.items():
            console.print(f"{tag_type}: {', '.join(tag_list)}")

    # Relations
    relations = db.get_profile_relations(profile.id)
    if relations:
        console.print("\n[bold]--- Relations ---[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Contact")
        table.add_column("Type")
        table.add_column("Note")

        for rel in relations:
            rel_name = get_contact_name(rel.related_contact_id)
            table.add_row(rel_name, rel.relation_type, rel.note or "-")

        console.print(table)

    console.print(f"\nLast Updated: {profile.updated_at}")


@profile_app.command("get-by-name")
def get_by_name(name: str = typer.Argument(..., help="Contact name")):
    """Search contact by name and view profile"""
    # Search contacts
    contacts = db.list_contacts(search=name)
    if not contacts:
        console.print(f"[yellow]No contact found matching '{name}'[/yellow]")
        return

    # If only one, show profile directly
    if len(contacts) == 1:
        get(contacts[0].id)
        return

    # If multiple, let user choose
    console.print(f"[yellow]Found {len(contacts)} contacts:[/yellow]")
    for c in contacts:
        console.print(f"  {c.id}: {c.name} ({c.category}) - {c.company or '-'}")

    console.print("\n请使用 ID 查询: my-secretary profile get <id>")


@profile_app.command("update")
def update(
    contact_id: int = typer.Argument(..., help="Contact ID"),
    personality: Optional[str] = typer.Option(None, "--personality", help="Personality description"),
    current_status: Optional[str] = typer.Option(None, "--status", help="Current status (busy/free/on-leave)"),
    status_note: Optional[str] = typer.Option(None, "--status-note", help="Status note"),
):
    """Update contact profile"""
    # Check if contact exists
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    updated = db.update_profile(
        contact_id,
        personality=personality,
        current_status=current_status,
        status_note=status_note,
    )

    if updated:
        console.print(f"[green]Profile updated for {contact.name}[/green]")
    else:
        console.print("[yellow]No changes made[/yellow]")


# Tag sub-commands
tag_app = typer.Typer(help="Manage profile tags")
profile_app.add_typer(tag_app, name="tag")


@tag_app.command("add")
def tag_add(
    contact_id: int = typer.Argument(..., help="Contact ID"),
    tag: str = typer.Option(..., "--tag", help="Tag name"),
    tag_type: str = typer.Option(..., "--type", help="Tag type (personality/skill/interest/other)"),
):
    """Add a tag to contact profile"""
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    if tag_type not in ["personality", "skill", "interest", "other"]:
        console.print("[red]Tag type must be one of: personality, skill, interest, other[/red]")
        raise typer.Exit(1)

    # Ensure profile exists
    profile = db.get_or_create_profile(contact_id)
    db.add_profile_tag(profile.id, tag, tag_type)
    console.print(f"[green]Tag '{tag}' ({tag_type}) added to {contact.name}[/green]")


@tag_app.command("list")
def tag_list(contact_id: int = typer.Argument(..., help="Contact ID")):
    """List all tags for contact profile"""
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    profile = db.get_profile(contact_id)
    if not profile:
        console.print("[yellow]No profile exists for this contact[/yellow]")
        return

    tags = db.get_profile_tags(profile.id)
    if not tags:
        console.print("[yellow]No tags yet[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Tag")
    table.add_column("Type")
    table.add_column("Created")

    for tag in tags:
        table.add_row(tag.tag, tag.tag_type, tag.created_at.strftime("%Y-%m-%d") if tag.created_at else "-")

    console.print(f"[bold]Tags for {contact.name}:[/bold]")
    console.print(table)


@tag_app.command("delete")
def tag_delete(
    contact_id: int = typer.Argument(..., help="Contact ID"),
    tag: str = typer.Option(..., "--tag", help="Tag name to delete"),
):
    """Delete a tag from contact profile"""
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    profile = db.get_profile(contact_id)
    if not profile:
        console.print("[yellow]No profile exists for this contact[/yellow]")
        return

    deleted = db.delete_profile_tag(profile.id, tag)
    if deleted:
        console.print(f"[green]Tag '{tag}' deleted[/green]")
    else:
        console.print(f"[red]Tag '{tag}' not found[/red]")
        raise typer.Exit(1)


# Relation sub-commands
relation_app = typer.Typer(help="Manage profile relations")
profile_app.add_typer(relation_app, name="relation")


@relation_app.command("add")
def relation_add(
    contact_id: int = typer.Argument(..., help="Contact ID"),
    related: int = typer.Option(..., "--related", help="Related contact ID"),
    relation_type: str = typer.Option(..., "--type", help="Relation type (colleague/leader/subordinate/friend/other)"),
    note: Optional[str] = typer.Option(None, "--note", help="Relation note"),
):
    """Add a relation to contact profile"""
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    related_contact = db.get_contact(related)
    if not related_contact:
        console.print(f"[red]Related contact {related} not found[/red]")
        raise typer.Exit(1)

    if relation_type not in ["colleague", "leader", "subordinate", "friend", "other"]:
        console.print("[red]Relation type must be one of: colleague, leader, subordinate, friend, other[/red]")
        raise typer.Exit(1)

    # Ensure profile exists
    profile = db.get_or_create_profile(contact_id)
    db.add_profile_relation(profile.id, related, relation_type, note)
    console.print(f"[green]Relation with {related_contact.name} added to {contact.name}[/green]")


@relation_app.command("list")
def relation_list(contact_id: int = typer.Argument(..., help="Contact ID")):
    """List all relations for contact profile"""
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    profile = db.get_profile(contact_id)
    if not profile:
        console.print("[yellow]No profile exists for this contact[/yellow]")
        return

    relations = db.get_profile_relations(profile.id)
    if not relations:
        console.print("[yellow]No relations yet[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Related Contact")
    table.add_column("Type")
    table.add_column("Note")
    table.add_column("Created")

    for rel in relations:
        rel_name = get_contact_name(rel.related_contact_id)
        table.add_row(rel_name, rel.relation_type, rel.note or "-", rel.created_at.strftime("%Y-%m-%d") if rel.created_at else "-")

    console.print(f"[bold]Relations for {contact.name}:[/bold]")
    console.print(table)


@relation_app.command("delete")
def relation_delete(
    contact_id: int = typer.Argument(..., help="Contact ID"),
    related: int = typer.Option(..., "--related", help="Related contact ID to remove"),
):
    """Delete a relation from contact profile"""
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    profile = db.get_profile(contact_id)
    if not profile:
        console.print("[yellow]No profile exists for this contact[/yellow]")
        return

    deleted = db.delete_profile_relation(profile.id, related)
    if deleted:
        console.print(f"[green]Relation with contact {related} deleted[/green]")
    else:
        console.print(f"[red]Relation with contact {related} not found[/red]")
        raise typer.Exit(1)


# Project sub-commands
project_app = typer.Typer(help="Manage profile projects")
profile_app.add_typer(project_app, name="project")


@project_app.command("add")
def project_add(
    contact_id: int = typer.Argument(..., help="Contact ID"),
    project: str = typer.Option(..., "--project", help="Project name"),
):
    """Add a project to contact profile"""
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    profile = db.get_or_create_profile(contact_id)

    # Get current projects
    current_projects = []
    if profile.projects:
        try:
            current_projects = json.loads(profile.projects)
        except json.JSONDecodeError:
            current_projects = []

    if project not in current_projects:
        current_projects.append(project)

    db.update_profile(contact_id, projects=json.dumps(current_projects))
    console.print(f"[green]Project '{project}' added to {contact.name}[/green]")


@project_app.command("list")
def project_list(contact_id: int = typer.Argument(..., help="Contact ID")):
    """List all projects for contact profile"""
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    profile = db.get_profile(contact_id)
    if not profile:
        console.print("[yellow]No profile exists for this contact[/yellow]")
        return

    if not profile.projects:
        console.print("[yellow]No projects yet[/yellow]")
        return

    try:
        projects = json.loads(profile.projects)
    except json.JSONDecodeError:
        projects = [profile.projects]

    if not projects:
        console.print("[yellow]No projects yet[/yellow]")
        return

    console.print(f"[bold]Projects for {contact.name}:[/bold]")
    for p in projects:
        console.print(f"  - {p}")


@project_app.command("delete")
def project_delete(
    contact_id: int = typer.Argument(..., help="Contact ID"),
    project: str = typer.Option(..., "--project", help="Project name to delete"),
):
    """Delete a project from contact profile"""
    contact = db.get_contact(contact_id)
    if not contact:
        console.print("[red]Contact not found[/red]")
        raise typer.Exit(1)

    profile = db.get_profile(contact_id)
    if not profile:
        console.print("[yellow]No profile exists for this contact[/yellow]")
        return

    current_projects = []
    if profile.projects:
        try:
            current_projects = json.loads(profile.projects)
        except json.JSONDecodeError:
            current_projects = []

    if project in current_projects:
        current_projects.remove(project)
        db.update_profile(contact_id, projects=json.dumps(current_projects))
        console.print(f"[green]Project '{project}' deleted[/green]")
    else:
        console.print(f"[red]Project '{project}' not found[/red]")
        raise typer.Exit(1)
