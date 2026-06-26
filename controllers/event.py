from database import get_session
from models.event import Event
from models.contract import Contract
from models.collaborator import Role, Collaborator
from controllers.auth import get_current_user
from datetime import datetime

def create_event(name: str, contract_id: int, start_date: datetime, end_date: datetime, location: str, attendees: int, notes: str) -> Event | None:
    current_user = get_current_user()
    if not current_user or current_user.role != Role.commercial:
        print("Accès refusé : seul un commercial peut créer un événement.")
        return None

    session = get_session()
    contract = session.get(Contract, contract_id)
    if not contract:
        print("Contrat introuvable.")
        return None

    if not contract.is_signed:
        print("Impossible de créer un événement : le contrat n'est pas signé.")
        return None

    if contract.commercial_id != current_user.id:
        print("Accès refusé : ce contrat ne vous appartient pas.")
        return None

    event = Event(
        name=name,
        contract_id=contract_id,
        client_id=contract.client_id,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support_id=None
    )
    session.add(event)
    session.commit()
    print(f"Événement {name} créé avec succès.")
    return event

def assign_support(event_id: int, support_id: int) -> Event | None:
    current_user = get_current_user()
    if not current_user or current_user.role != Role.gestion:
        print("Accès refusé : seul un gestionnaire peut assigner un support.")
        return None

    session = get_session()
    event = session.get(Event, event_id)
    if not event:
        print("Événement introuvable.")
        return None

    support = session.get(Collaborator, support_id)
    if not support or support.role != Role.support:
        print("Collaborateur introuvable ou n'est pas du support.")
        return None

    event.support_id = support_id
    session.commit()
    print(f"Support {support.first_name} {support.last_name} assigné à l'événement {event.name}.")
    return event

def update_event(event_id: int, **kwargs) -> Event | None:
    current_user = get_current_user()
    if not current_user:
        return None

    session = get_session()
    event = session.get(Event, event_id)
    if not event:
        print("Événement introuvable.")
        return None

    if current_user.role == Role.support and event.support_id != current_user.id:
        print("Accès refusé : vous n'êtes pas responsable de cet événement.")
        return None

    if current_user.role == Role.commercial:
        print("Accès refusé : un commercial ne peut pas modifier un événement.")
        return None

    for key, value in kwargs.items():
        setattr(event, key, value)

    session.commit()
    print(f"Événement {event.name} mis à jour.")
    return event

def get_all_events() -> list[Event]:
    session = get_session()
    return session.query(Event).all()

def get_my_events() -> list[Event]:
    current_user = get_current_user()
    if not current_user:
        return []
    session = get_session()
    return session.query(Event).filter_by(support_id=current_user.id).all()

def get_events_without_support() -> list[Event]:
    session = get_session()
    return session.query(Event).filter(Event.support_id == None).all()