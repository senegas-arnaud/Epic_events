from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum
from models.base import Base
import enum

class Role(enum.Enum):
    gestion = "gestion"
    commercial = "commercial"
    support = "support"

class Collaborator(Base):
    __tablename__ = "collaborators"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)

    def __repr__(self):
        return f"<Collaborator {self.first_name} {self.last_name} ({self.role.value})>"