from pydantic import BaseModel, ConfigDict, field_validator

from src.trade.models import Direction


class TradeView(BaseModel):
    id: int
    ticket: str
    direction: Direction

    model_config = ConfigDict(from_attributes=True)

class TradeCreate(BaseModel):
    ticket: str
    direction: Direction

    @field_validator('ticket')
    def name_must_be_capitalized(cls, v):
        if not v.isupper():
            raise ValueError('Product name must start with a capital letter')
        return v