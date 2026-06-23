import bcrypt
import jwt
import json
import os
from datetime import datetime, timedelta, timezone
from database import get_session
from models.collaborator import Collaborator
from config import SECRET_KEY

TOKEN_FILE = ".token"
TOKEN_EXPIRATION_HOURS = 24

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def generate_token(collaborator: Collaborator) -> str:
    payload = {
        "user_id": collaborator.id,
        "role": collaborator.role.value,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def save_token(token: str):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token}, f)

def load_token() -> str | None:
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
        return data.get("token")

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print("Session expirée, veuillez vous reconnecter.")
        os.remove(TOKEN_FILE)
        return None
    except jwt.InvalidTokenError:
        print("Token invalide.")
        return None

def get_current_user() -> Collaborator | None:
    token = load_token()
    if not token:
        print("Vous n'êtes pas connecté.")
        return None

    payload = decode_token(token)
    if not payload:
        return None

    session = get_session()
    return session.get(Collaborator, payload["user_id"])

def login(email: str, password: str) -> bool:
    session = get_session()
    collaborator = session.query(Collaborator).filter_by(email=email).first()

    if not collaborator or not verify_password(password, collaborator.password_hash):
        print("Email ou mot de passe incorrect.")
        return False

    token = generate_token(collaborator)
    save_token(token)
    print(f"Bienvenue {collaborator.first_name} !")
    return True

def logout():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print("Déconnecté avec succès.")

def create_admin(email: str, password: str, first_name: str, last_name: str):
    session = get_session()
    existing = session.query(Collaborator).filter_by(email=email).first()
    if existing:
        print("Un collaborateur avec cet email existe déjà.")
        return

    from models.collaborator import Role
    admin = Collaborator(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=hash_password(password),
        role=Role.gestion
    )
    session.add(admin)
    session.commit()
    print(f"Gestionnaire {first_name} {last_name} créé avec succès.")