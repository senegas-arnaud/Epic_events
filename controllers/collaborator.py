from database import get_session
from models.collaborator import Collaborator, Role
from controllers.auth import hash_password, get_current_user

def create_collaborator(first_name: str, last_name: str, email: str, password: str, role: str) -> Collaborator | None:
    current_user = get_current_user()
    if not current_user or current_user.role != Role.gestion:
        print("Accès refusé : seul un gestionnaire peut créer un collaborateur.")
        return None

    session = get_session()
    existing = session.query(Collaborator).filter_by(email=email).first()
    if existing:
        print("Un collaborateur avec cet email existe déjà.")
        return None

    try:
        role_enum = Role(role)
    except ValueError:
        print(f"Rôle invalide. Choisissez parmi : {[r.value for r in Role]}")
        return None

    collaborator = Collaborator(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=hash_password(password),
        role=role_enum
    )
    session.add(collaborator)
    session.commit()
    print(f"Collaborateur {first_name} {last_name} créé avec succès.")
    return collaborator

def update_collaborator(collaborator_id: int, **kwargs) -> Collaborator | None:
    current_user = get_current_user()
    if not current_user or current_user.role != Role.gestion:
        print("Accès refusé : seul un gestionnaire peut modifier un collaborateur.")
        return None

    session = get_session()
    collaborator = session.get(Collaborator, collaborator_id)
    if not collaborator:
        print("Collaborateur introuvable.")
        return None

    for key, value in kwargs.items():
        if key == "password":
            setattr(collaborator, "password_hash", hash_password(value))
        elif key == "role":
            try:
                setattr(collaborator, "role", Role(value))
            except ValueError:
                print(f"Rôle invalide. Choisissez parmi : {[r.value for r in Role]}")
                return None
        else:
            setattr(collaborator, key, value)

    session.commit()
    print(f"Collaborateur {collaborator.first_name} {collaborator.last_name} mis à jour.")
    return collaborator

def delete_collaborator(collaborator_id: int) -> bool:
    current_user = get_current_user()
    if not current_user or current_user.role != Role.gestion:
        print("Accès refusé : seul un gestionnaire peut supprimer un collaborateur.")
        return False

    session = get_session()
    collaborator = session.get(Collaborator, collaborator_id)
    if not collaborator:
        print("Collaborateur introuvable.")
        return False

    session.delete(collaborator)
    session.commit()
    print(f"Collaborateur {collaborator.first_name} {collaborator.last_name} supprimé.")
    return True

def get_all_collaborators() -> list[Collaborator]:
    session = get_session()
    return session.query(Collaborator).all()