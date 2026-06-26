from database import get_session
from models.client import Client
from models.collaborator import Role
from controllers.auth import get_current_user
from datetime import datetime

def create_client(full_name: str, email: str, phone: str, company_name: str) -> Client | None:
    current_user = get_current_user()
    if not current_user or current_user.role != Role.commercial:
        print("Accès refusé : seul un commercial peut créer un client.")
        return None

    session = get_session()
    existing = session.query(Client).filter_by(email=email).first()
    if existing:
        print("Un client avec cet email existe déjà.")
        return None

    client = Client(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
        commercial_id=current_user.id
    )
    session.add(client)
    session.commit()
    print(f"Client {full_name} créé avec succès.")
    return client

def update_client(client_id: int, **kwargs) -> Client | None:
    current_user = get_current_user()
    if not current_user or current_user.role != Role.commercial:
        print("Accès refusé : seul un commercial peut modifier un client.")
        return None

    session = get_session()
    client = session.get(Client, client_id)
    if not client:
        print("Client introuvable.")
        return None

    if client.commercial_id != current_user.id:
        print("Accès refusé : vous n'êtes pas responsable de ce client.")
        return None

    for key, value in kwargs.items():
        setattr(client, key, value)

    client.updated_at = datetime.utcnow()
    session.commit()
    print(f"Client {client.full_name} mis à jour.")
    return client

def get_all_clients() -> list[Client]:
    session = get_session()
    return session.query(Client).all()

def get_my_clients() -> list[Client]:
    current_user = get_current_user()
    if not current_user:
        return []

    session = get_session()
    return session.query(Client).filter_by(commercial_id=current_user.id).all()