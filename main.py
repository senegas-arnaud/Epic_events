from database import init_db
import controllers
import views
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def show_menu(current_user):
    console.print(f"\n[bold cyan]Connecté en tant que {current_user.first_name} ({current_user.role.value})[/bold cyan]")
    console.print("\n[bold]Que voulez-vous faire ?[/bold]")

    options = {
        "1": "Voir tous les collaborateurs",
        "2": "Voir tous les clients",
        "3": "Voir tous les contrats",
        "4": "Voir tous les événements",
    }

    from models.collaborator import Role

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

def handle_gestion(choice, current_user):
    from models.collaborator import Role
    if choice == "5":
        data = views.prompt_new_collaborator()
        controllers.create_collaborator(**data)
    elif choice == "6":
        collaborator_id = int(Prompt.ask("ID du collaborateur à modifier"))
        field = Prompt.ask("Champ à modifier", choices=["first_name", "last_name", "email", "password", "role"])
        value = Prompt.ask("Nouvelle valeur")
        controllers.update_collaborator(collaborator_id, **{field: value})
    elif choice == "7":
        collaborator_id = int(Prompt.ask("ID du collaborateur à supprimer"))
        if controllers.confirm_action("Confirmer la suppression ?"):
            controllers.delete_collaborator(collaborator_id)
    elif choice == "8":
        data = views.prompt_new_contract()
        controllers.create_contract(**data)
    elif choice == "9":
        contract_id = int(Prompt.ask("ID du contrat à modifier"))
        field = Prompt.ask("Champ à modifier", choices=["total_amount", "remaining_amount", "is_signed"])
        value = Prompt.ask("Nouvelle valeur")
        if field == "is_signed":
            value = value.lower() == "true"
        elif field in ["total_amount", "remaining_amount"]:
            value = float(value)
        controllers.update_contract(contract_id, **{field: value})
    elif choice == "10":
        event_id = int(Prompt.ask("ID de l'événement"))
        support_id = int(Prompt.ask("ID du collaborateur support"))
        controllers.assign_support(event_id, support_id)
    elif choice == "11":
        events = controllers.get_events_without_support()
        views.display_events(events)

def handle_commercial(choice, current_user):
    if choice == "5":
        data = views.prompt_new_client()
        controllers.create_client(**data)
    elif choice == "6":
        client_id = int(Prompt.ask("ID du client à modifier"))
        field = Prompt.ask("Champ à modifier", choices=["full_name", "email", "phone", "company_name"])
        value = Prompt.ask("Nouvelle valeur")
        controllers.update_client(client_id, **{field: value})
    elif choice == "7":
        clients = controllers.get_my_clients()
        views.display_clients(clients)
    elif choice == "8":
        contracts = controllers.get_my_contracts()
        views.display_contracts(contracts)
    elif choice == "9":
        contracts = controllers.get_unsigned_contracts()
        views.display_contracts(contracts)
    elif choice == "10":
        contracts = controllers.get_unpaid_contracts()
        views.display_contracts(contracts)
    elif choice == "11":
        data = views.prompt_new_event()
        controllers.create_event(**data)

def handle_support(choice, current_user):
    if choice == "5":
        events = controllers.get_my_events()
        views.display_events(events)
    elif choice == "6":
        event_id = int(Prompt.ask("ID de l'événement à modifier"))
        field = Prompt.ask("Champ à modifier", choices=["location", "attendees", "notes"])
        value = Prompt.ask("Nouvelle valeur")
        if field == "attendees":
            value = int(value)
        controllers.update_event(event_id, **{field: value})

def main():
    init_db()
    from models.collaborator import Role

    console.print("[bold magenta]Bienvenue sur Epic Events CRM[/bold magenta]")

    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        console.print("\n[bold]Création du premier gestionnaire[/bold]")
        data = views.prompt_new_collaborator()
        controllers.create_first_admin(
            email=data["email"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"]
        )
        return

    current_user = controllers.get_current_user()
    if not current_user:
        email, password = views.prompt_login()
        if not controllers.login(email, password):
            return
        current_user = controllers.get_current_user()

    while True:
        choice = show_menu(current_user)

        if choice == "0":
            controllers.logout()
            break
        elif choice == "1":
            views.display_collaborators(controllers.get_all_collaborators())
        elif choice == "2":
            views.display_clients(controllers.get_all_clients())
        elif choice == "3":
            views.display_contracts(controllers.get_all_contracts())
        elif choice == "4":
            views.display_events(controllers.get_all_events())
        else:
            if current_user.role == Role.gestion:
                handle_gestion(choice, current_user)
            elif current_user.role == Role.commercial:
                handle_commercial(choice, current_user)
            elif current_user.role == Role.support:
                handle_support(choice, current_user)

if __name__ == "__main__":
    main()