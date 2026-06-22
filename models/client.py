from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from models.base import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.contract import Contract
    from models.collaborator import Collaborator

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    company_name: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    commercial_id: Mapped[int] = mapped_column(ForeignKey("collaborators.id"), nullable=False)

    commercial: Mapped["Collaborator"] = relationship("Collaborator")
    contracts: Mapped[list["Contract"]] = relationship("Contract", back_populates="client")

    def __repr__(self):
        return f"<Client {self.full_name} ({self.company_name})>"