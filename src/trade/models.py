import enum
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from src.database import Base


class Direction(enum.Enum):
    long = "Long"
    short = "Short"

class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket: Mapped[str]
    direction: Mapped[Direction]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
