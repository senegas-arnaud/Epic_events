from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

def display_collaborators(collaborators):
    table = Table(title="Collaborateurs", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Prénom", style="white")
    table.add_column("Nom", style="white")
    table.add_column("Email", style="green")
    table.add_column("Rôle", style="magenta")

    for c in collaborators:
        table.add_row(
            str(c.id),
            c.first_name,
            c.last_name,
            c.email,
            c.role.value
        )
    console.print(table)

def display_clients(clients):
    table = Table(title="Clients", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Nom complet", style="white")
    table.add_column("Email", style="green")
    table.add_column("Téléphone", style="white")
    table.add_column("Entreprise", style="yellow")
    table.add_column("Commercial ID", style="magenta")

    for c in clients:
        table.add_row(
            str(c.id),
            c.full_name,
            c.email,
            c.phone or "-",
            c.company_name or "-",
            str(c.commercial_id)
        )
    console.print(table)

def display_contracts(contracts):
    table = Table(title="Contrats", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Client ID", style="white")
    table.add_column("Montant total", style="green")
    table.add_column("Reste à payer", style="yellow")
    table.add_column("Signé", style="magenta")
    table.add_column("Date création", style="white")

    for c in contracts:
        signed = "[green]✓[/green]" if c.is_signed else "[red]✗[/red]"
        table.add_row(
            str(c.id),
            str(c.client_id),
            f"{c.total_amount}€",
            f"{c.remaining_amount}€",
            signed,
            c.created_at.strftime("%d/%m/%Y")
        )
    console.print(table)

def display_events(events):
    table = Table(title="Événements", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Nom", style="white")
    table.add_column("Client ID", style="white")
    table.add_column("Début", style="green")
    table.add_column("Fin", style="green")
    table.add_column("Lieu", style="yellow")
    table.add_column("Participants", style="white")
    table.add_column("Support ID", style="magenta")

    for e in events:
        table.add_row(
            str(e.id),
            e.name,
            str(e.client_id),
            e.start_date.strftime("%d/%m/%Y %H:%M"),
            e.end_date.strftime("%d/%m/%Y %H:%M"),
            e.location or "-",
            str(e.attendees or "-"),
            str(e.support_id) if e.support_id else "[red]Non assigné[/red]"
        )
    console.print(table)

def display_success(message: str):
    console.print(f"[bold green]✓ {message}[/bold green]")

def display_error(message: str):
    console.print(f"[bold red]✗ {message}[/bold red]")

def display_warning(message: str):
    console.print(f"[bold yellow]⚠ {message}[/bold yellow]")

def display_info(message: str):
    console.print(f"[bold cyan]ℹ {message}[/bold cyan]")