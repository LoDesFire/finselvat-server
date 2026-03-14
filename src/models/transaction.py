import datetime
import uuid

from sqlalchemy import UUID, text, INT, TEXT, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Transaction(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid()"),
    )
    transaction_type: Mapped[int] = mapped_column(
        INT,
        nullable=False,
    )
    data: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    sign: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    signer_cert: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )
    transaction_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    transaction_metadata: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,
        name="metadata",
    )
    transaction_in: Mapped[str] = mapped_column(
        String(64),
        nullable=True,
    )
    transaction_out: Mapped[str] = mapped_column(
        String(64),
        nullable=True,
    )
    message_receiver_batch: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
    )
