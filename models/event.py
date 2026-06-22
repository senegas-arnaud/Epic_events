from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Integer, Text
from models.base import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.contract import Contract
    from models.client import Client
    from models.collaborator import Collaborator

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    attendees: Mapped[int] = mapped_column(Integer, nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    support_id: Mapped[int] = mapped_column(ForeignKey("collaborators.id"), nullable=True)

    contract: Mapped["Contract"] = relationship("Contract", back_populates="event")
    client: Mapped["Client"] = relationship("Client")
    support: Mapped["Collaborator"] = relationship("Collaborator")

    def __repr__(self):
        return f"<Event {self.name} - {self.start_date.strftime('%d/%m/%Y')}>"