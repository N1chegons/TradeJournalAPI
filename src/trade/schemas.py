import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.trade.models import Direction


class TradeView(BaseModel):
    id: int
    ticket: str
    PnL: float
    added_at: datetime.datetime

    @field_validator('added_at')
    def custom(cls, v):
        return datetime.datetime.strftime(v, "%m.%d.%Y")

    model_config = ConfigDict(from_attributes=True)

class TradeViewAll(BaseModel):
    id: int
    ticket: str
    direction: Direction
    entry_price: float
    exit_price: float
    quantity: float
    PnL: float
    added_at: datetime.datetime

    @field_validator('added_at')
    def custom(cls, v):
        return datetime.datetime.strftime(v, "%m.%d.%Y")

    model_config = ConfigDict(from_attributes=True)

class TradeCreate(BaseModel):
    ticket: str
    direction: Direction
    entry_price: float = Field(ge=0)
    exit_price: float = Field(ge=0)
    quantity: float = Field(ge=0)
