from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Boolean, Float
from models.base import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.client import Client
    from models.collaborator import Collaborator
    from models.event import Event

class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    commercial_id: Mapped[int] = mapped_column(ForeignKey("collaborators.id"), nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    remaining_amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_signed: Mapped[bool] = mapped_column(Boolean, default=False)

    client: Mapped["Client"] = relationship("Client", back_populates="contracts")
    commercial: Mapped["Collaborator"] = relationship("Collaborator")
    event: Mapped["Event"] = relationship("Event", back_populates="contract")

    def __repr__(self):
        return f"<Contract {self.id} - {self.client} ({'signé' if self.is_signed else 'non signé'})>"