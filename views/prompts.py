from rich.console import Console
from rich.prompt import Prompt, Confirm
from datetime import datetime
from utils.validators import (
    validate_email, validate_phone,
    validate_date, validate_positive_float,
    validate_positive_int
)

console = Console()
CANCEL = "__cancel__"

def cancelled(value) -> bool:
    return value == CANCEL

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_with_cancel(message: str, password: bool = False) -> str:
    if not password:
        console.print("[dim]Tapez 0 pour annuler[/dim]")
    value = Prompt.ask(message, password=password)
    if value == "0":
        return CANCEL
    return value

def prompt_email() -> str | None:
    while True:
        email = prompt_with_cancel("Email")
        if cancelled(email):
            return None
        if validate_email(email):
            return email
        console.print("[red]Email invalide, réessayez.[/red]")

def prompt_phone() -> str | None:
    while True:
        phone = prompt_with_cancel("Téléphone")
        if cancelled(phone):
            return None
        if validate_phone(phone):
            return phone
        console.print("[red]Téléphone invalide, réessayez.[/red]")

def prompt_float(message: str) -> float | None:
    while True:
        value = prompt_with_cancel(message)
        if cancelled(value):
            return None
        result = validate_positive_float(value)
        if result is not None:
            return result
        console.print("[red]Valeur invalide, entrez un nombre positif.[/red]")

def prompt_int(message: str) -> int | None:
    while True:
        value = prompt_with_cancel(message)
        if cancelled(value):
            return None
        result = validate_positive_int(value)
        if result is not None:
            return result
        console.print("[red]Valeur invalide, entrez un nombre entier positif.[/red]")

def prompt_date(message: str) -> datetime | None:
    while True:
        value = prompt_with_cancel(f"{message} (DD/MM/YYYY HH:MM)")
        if cancelled(value):
            return None
        result = validate_date(value)
        if result is not None:
            return result
        console.print("[red]Date invalide, format attendu : DD/MM/YYYY HH:MM[/red]")

def prompt_login() -> tuple[str, str]:
    clear_screen()
    console.print("\n[bold cyan]CONNEXION[/bold cyan]", justify="center")
    console.print("[dim]─────────────────────────────[/dim]\n", justify="center")
    email = Prompt.ask("Email")
    password = Prompt.ask("Mot de passe", password=True)
    return email, password

def prompt_new_collaborator() -> dict | None:
    clear_screen()
    console.print("\n[bold cyan]Nouveau collaborateur[/bold cyan]", justify="center")
    console.print("[dim]─────────────────────────────[/dim]\n", justify="center")

    first_name = prompt_with_cancel("Prénom")
    if cancelled(first_name): return None

    last_name = prompt_with_cancel("Nom")
    if cancelled(last_name): return None

    email = prompt_email()
    if email is None: return None

    password = Prompt.ask("Mot de passe", password=True)

    role = Prompt.ask("Rôle", choices=["gestion", "commercial", "support", "0"])
    if role == "0": return None

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "role": role
    }

def prompt_new_client() -> dict | None:
    clear_screen()
    console.print("\n[bold cyan]Nouveau client[/bold cyan]", justify="center")
    console.print("[dim]─────────────────────────────[/dim]\n", justify="center")

    full_name = prompt_with_cancel("Nom complet")
    if cancelled(full_name): return None

    email = prompt_email()
    if email is None: return None

    phone = prompt_phone()
    if phone is None: return None

    company_name = prompt_with_cancel("Entreprise")
    if cancelled(company_name): return None

    return {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "company_name": company_name
    }

def prompt_new_contract() -> dict | None:
    clear_screen()
    console.print("\n[bold cyan]Nouveau contrat[/bold cyan]", justify="center")
    console.print("[dim]─────────────────────────────[/dim]\n", justify="center")

    client_id = prompt_int("ID du client")
    if client_id is None: return None

    total_amount = prompt_float("Montant total")
    if total_amount is None: return None

    remaining_amount = prompt_float("Montant restant")
    if remaining_amount is None: return None

    return {
        "client_id": client_id,
        "total_amount": total_amount,
        "remaining_amount": remaining_amount
    }

def prompt_new_event() -> dict | None:
    clear_screen()
    console.print("\n[bold cyan]Nouvel événement[/bold cyan]", justify="center")
    console.print("[dim]─────────────────────────────[/dim]\n", justify="center")

    name = prompt_with_cancel("Nom de l'événement")
    if cancelled(name): return None

    contract_id = prompt_int("ID du contrat")
    if contract_id is None: return None

    start_date = prompt_date("Date début")
    if start_date is None: return None

    end_date = prompt_date("Date fin")
    if end_date is None: return None

    if end_date <= start_date:
        console.print("[red]La date de fin doit être après la date de début.[/red]")
        return None

    location = prompt_with_cancel("Lieu")
    if cancelled(location): return None

    attendees = prompt_int("Nombre de participants")
    if attendees is None: return None

    notes = prompt_with_cancel("Notes")
    if cancelled(notes): return None

    return {
        "name": name,
        "contract_id": contract_id,
        "start_date": start_date,
        "end_date": end_date,
        "location": location,
        "attendees": attendees,
        "notes": notes
    }

def confirm_action(message: str) -> bool:
    return Confirm.ask(message)