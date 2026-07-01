from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich import box

console = Console()

def prompt_login() -> tuple[str, str]:
    console.print("\n[bold cyan]Connexion Epic Events[/bold cyan]")
    email = Prompt.ask("Email")
    password = Prompt.ask("Mot de passe", password=True)
    return email, password

def prompt_new_collaborator() -> dict:
    console.print("\n[bold cyan]Nouveau collaborateur[/bold cyan]")
    return {
        "first_name": Prompt.ask("Prénom"),
        "last_name": Prompt.ask("Nom"),
        "email": Prompt.ask("Email"),
        "password": Prompt.ask("Mot de passe", password=True),
        "role": Prompt.ask("Rôle", choices=["gestion", "commercial", "support"])
    }

def prompt_new_client() -> dict:
    console.print("\n[bold cyan]Nouveau client[/bold cyan]")
    return {
        "full_name": Prompt.ask("Nom complet"),
        "email": Prompt.ask("Email"),
        "phone": Prompt.ask("Téléphone", default=""),
        "company_name": Prompt.ask("Entreprise", default="")
    }

def prompt_new_contract() -> dict:
    console.print("\n[bold cyan]Nouveau contrat[/bold cyan]")
    return {
        "client_id": int(Prompt.ask("ID du client")),
        "total_amount": float(Prompt.ask("Montant total")),
        "remaining_amount": float(Prompt.ask("Montant restant"))
    }

def prompt_new_event() -> dict:
    from datetime import datetime
    console.print("\n[bold cyan]Nouvel événement[/bold cyan]")
    return {
        "name": Prompt.ask("Nom de l'événement"),
        "contract_id": int(Prompt.ask("ID du contrat")),
        "start_date": datetime.strptime(Prompt.ask("Date début (DD/MM/YYYY HH:MM)"), "%d/%m/%Y %H:%M"),
        "end_date": datetime.strptime(Prompt.ask("Date fin (DD/MM/YYYY HH:MM)"), "%d/%m/%Y %H:%M"),
        "location": Prompt.ask("Lieu", default=""),
        "attendees": int(Prompt.ask("Nombre de participants", default="0")),
        "notes": Prompt.ask("Notes", default="")
    }

def confirm_action(message: str) -> bool:
    return Confirm.ask(message)