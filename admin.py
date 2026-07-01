from database import init_db
from controllers.auth import create_admin

init_db()
create_admin(
        email="admin@epic.com",
        password="admin123",
        first_name="Arnaud",
        last_name="Senegas"
    )