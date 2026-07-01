from database import init_db
import controllers
import views
from views.prompts import clear_screen
from rich.console import Console
from rich.prompt import Prompt
from utils.validators import validate_positive_int, validate_positive_float

console = Console()


def prompt_int_inline(message: str) -> int | None:
    console.print("[dim]Tapez 0 pour annuler[/dim]")
    value = Prompt.ask(message)
    if value == "0":
        return None
    result = validate_positive_int(value)
    if result is None:
        console.print("[red]ID invalide.[/red]")
        return None
    return result


def show_menu(current_user):
    from models.collaborator import Role
    clear_screen()
    console.print("\n[bold magenta]EPIC EVENTS CRM[/bold magenta]", justify="center")
    console.print("[dim]─────────────────────────────[/dim]\n", justify="center")
    console.print(f"[bold cyan]Connecté : {current_user.first_name} {current_user.last_name} ({current_user.role.value})[/bold cyan]", justify="center")
    console.print("\n[bold]Que voulez-vous faire ?[/bold]")

    options = {
        "1": "Voir tous les collaborateurs",
        "2": "Voir tous les clients",
        "3": "Voir tous les contrats",
        "4": "Voir tous les événements",
    }

    if current_user.role == Role.gestion:
        options.update({
            "5": "Créer un collaborateur",
            "6": "Modifier un collaborateur",
            "7": "Supprimer un collaborateur",
            "8": "Créer un contrat",
            "9": "Modifier un contrat",
            "10": "Assigner un support à un événement",
            "11": "Voir les événements sans support",
        })
    elif current_user.role == Role.commercial:
        options.update({
            "5": "Créer un client",
            "6": "Modifier un client",
            "7": "Voir mes clients",
            "8": "Voir mes contrats",
            "9": "Voir les contrats non signés",
            "10": "Voir les contrats non payés",
            "11": "Créer un événement",
        })
    elif current_user.role == Role.support:
        options.update({
            "5": "Voir mes événements",
            "6": "Modifier un événement",
        })

    options["0"] = "Se déconnecter"

    for key, value in options.items():
        console.print(f"  [cyan]{key}[/cyan] — {value}")

    return Prompt.ask("\nVotre choix", choices=list(options.keys()))


def handle_gestion(choice):
    try:
        if choice == "5":
            data = views.prompt_new_collaborator()
            if data:
                controllers.create_collaborator(**data)

        elif choice == "6":
            clear_screen()
            collaborator_id = prompt_int_inline("ID du collaborateur à modifier")
            if collaborator_id is None: return
            field = Prompt.ask("Champ à modifier", choices=["first_name", "last_name", "email", "password", "role", "0"])
            if field == "0": return
            value = Prompt.ask("Nouvelle valeur")
            controllers.update_collaborator(collaborator_id, **{field: value})

        elif choice == "7":
            clear_screen()
            collaborator_id = prompt_int_inline("ID du collaborateur à supprimer")
            if collaborator_id is None: return
            if views.confirm_action("Confirmer la suppression ?"):
                controllers.delete_collaborator(collaborator_id)

        elif choice == "8":
            data = views.prompt_new_contract()
            if data:
                controllers.create_contract(**data)

        elif choice == "9":
            clear_screen()
            contract_id = prompt_int_inline("ID du contrat à modifier")
            if contract_id is None: return
            field = Prompt.ask("Champ à modifier", choices=["total_amount", "remaining_amount", "is_signed", "0"])
            if field == "0": return
            value = Prompt.ask("Nouvelle valeur")
            if field == "is_signed":
                value = value.lower() == "true"
            elif field in ["total_amount", "remaining_amount"]:
                result = validate_positive_float(value)
                if result is None:
                    console.print("[red]Valeur invalide.[/red]")
                    return
                value = result
            controllers.update_contract(contract_id, **{field: value})

        elif choice == "10":
            clear_screen()
            event_id = prompt_int_inline("ID de l'événement")
            if event_id is None: return
            support_id = prompt_int_inline("ID du collaborateur support")
            if support_id is None: return
            controllers.assign_support(event_id, support_id)

        elif choice == "11":
            clear_screen()
            views.display_events(controllers.get_events_without_support())

    except Exception as e:
        console.print(f"[red]Une erreur est survenue : {e}[/red]")


def handle_commercial(choice):
    try:
        if choice == "5":
            data = views.prompt_new_client()
            if data:
                controllers.create_client(**data)

        elif choice == "6":
            clear_screen()
            client_id = prompt_int_inline("ID du client à modifier")
            if client_id is None: return
            field = Prompt.ask("Champ à modifier", choices=["full_name", "email", "phone", "company_name", "0"])
            if field == "0": return
            value = Prompt.ask("Nouvelle valeur")
            controllers.update_client(client_id, **{field: value})

        elif choice == "7":
            clear_screen()
            views.display_clients(controllers.get_my_clients())

        elif choice == "8":
            clear_screen()
            views.display_contracts(controllers.get_my_contracts())

        elif choice == "9":
            clear_screen()
            views.display_contracts(controllers.get_unsigned_contracts())

        elif choice == "10":
            clear_screen()
            views.display_contracts(controllers.get_unpaid_contracts())

        elif choice == "11":
            data = views.prompt_new_event()
            if data:
                controllers.create_event(**data)

    except Exception as e:
        console.print(f"[red]Une erreur est survenue : {e}[/red]")


def handle_support(choice):
    try:
        if choice == "5":
            clear_screen()
            views.display_events(controllers.get_my_events())

        elif choice == "6":
            clear_screen()
            event_id = prompt_int_inline("ID de l'événement à modifier")
            if event_id is None: return
            field = Prompt.ask("Champ à modifier", choices=["location", "attendees", "notes", "0"])
            if field == "0": return
            value = Prompt.ask("Nouvelle valeur")
            if field == "attendees":
                result = validate_positive_int(value)
                if result is None:
                    console.print("[red]Valeur invalide.[/red]")
                    return
                value = result
            controllers.update_event(event_id, **{field: value})

    except Exception as e:
        console.print(f"[red]Une erreur est survenue : {e}[/red]")


def main():
    init_db()
    from models.collaborator import Role

    clear_screen()
    console.print("\n[bold magenta]EPIC EVENTS CRM[/bold magenta]", justify="center")
    console.print("[dim]─────────────────────────────[/dim]\n", justify="center")

    current_user = controllers.get_current_user()
    if not current_user:
        email, password = views.prompt_login()
        if not controllers.login(email, password):
            console.print("\n[red]Connexion échouée.[/red]", justify="center")
            return
        current_user = controllers.get_current_user()

    while True:
        choice = show_menu(current_user)

        if choice == "0":
            controllers.logout()
            clear_screen()
            console.print("\n[bold magenta]À bientôt ![/bold magenta]", justify="center")
            break
        elif choice == "1":
            clear_screen()
            views.display_collaborators(controllers.get_all_collaborators())
        elif choice == "2":
            clear_screen()
            views.display_clients(controllers.get_all_clients())
        elif choice == "3":
            clear_screen()
            views.display_contracts(controllers.get_all_contracts())
        elif choice == "4":
            clear_screen()
            views.display_events(controllers.get_all_events())
        else:
            if current_user.role == Role.gestion:
                handle_gestion(choice)
            elif current_user.role == Role.commercial:
                handle_commercial(choice)
            elif current_user.role == Role.support:
                handle_support(choice)

        Prompt.ask("\n[dim]Appuyez sur Entrée pour continuer[/dim]")


if __name__ == "__main__":
    main()