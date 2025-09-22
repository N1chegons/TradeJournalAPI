import enum
import datetime

from sqlalchemy import ForeignKey, text
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
    entry_price: Mapped[float]
    exit_price: Mapped[float]
    quantity: Mapped[float]
    PnL: Mapped[float] = mapped_column(nullable=True)
    added_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc',now())"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
