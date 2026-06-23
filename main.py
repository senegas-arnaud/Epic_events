from database import init_db
from controllers.auth import create_admin, login, logout
from controllers.collaborator import create_collaborator, get_all_collaborators

if __name__ == "__main__":
    init_db()

    create_admin(
        email="admin@epic.com",
        password="admin123",
        first_name="Arnaud",
        last_name="Senegas"
    )

    login("admin@epic.com", "admin123")

    create_collaborator(
        first_name="Jean",
        last_name="Jean",
        email="jean@epic.com",
        password="jean123",
        role="commercial"
    )

    collaborators = get_all_collaborators()
    for c in collaborators:
        print(c)