from database import get_session
from models.contract import Contract
from models.client import Client
from models.collaborator import Role
from controllers.auth import get_current_user

def create_contract(client_id: int, total_amount: float, remaining_amount: float) -> Contract | None:
    current_user = get_current_user()
    if not current_user or current_user.role != Role.gestion:
        print("Accès refusé : seul un gestionnaire peut créer un contrat.")
        return None

    session = get_session()
    client = session.get(Client, client_id)
    if not client:
        print("Client introuvable.")
        return None

    contract = Contract(
        client_id=client_id,
        commercial_id=client.commercial_id,
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        is_signed=False
    )
    session.add(contract)
    session.commit()
    print(f"Contrat créé avec succès pour le client {client.full_name}.")
    return contract

def update_contract(contract_id: int, **kwargs) -> Contract | None:
    current_user = get_current_user()
    if not current_user or current_user.role != Role.gestion:
        print("Accès refusé : seul un gestionnaire peut modifier un contrat.")
        return None

    session = get_session()
    contract = session.get(Contract, contract_id)
    if not contract:
        print("Contrat introuvable.")
        return None

    for key, value in kwargs.items():
        setattr(contract, key, value)

    session.commit()
    print(f"Contrat {contract_id} mis à jour.")
    return contract

def get_all_contracts() -> list[Contract]:
    session = get_session()
    return session.query(Contract).all()

def get_unsigned_contracts() -> list[Contract]:
    session = get_session()
    return session.query(Contract).filter_by(is_signed=False).all()

def get_unpaid_contracts() -> list[Contract]:
    session = get_session()
    return session.query(Contract).filter(Contract.remaining_amount > 0).all()

def get_my_contracts() -> list[Contract]:
    current_user = get_current_user()
    if not current_user:
        return []
    session = get_session()
    return session.query(Contract).filter_by(commercial_id=current_user.id).all()