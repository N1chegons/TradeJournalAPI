from fastapi import APIRouter, Depends

from src.auth.models import User
from src.auth.router import cur_user
from src.trade.repository import TradeRepository
from src.trade.schemas import TradeCreate

router = APIRouter(
    prefix="/trade",
    tags=["Journal"]
)

# get
@router.get("/get_trades/")
async def get_trades(limit: int = 10, user: User = Depends(cur_user)):
    trades = await TradeRepository.get_all_trades_journal(user, limit)
    return trades

# post
@router.post("/add_trade/", description="Write a ticket in XXX format.")
async def add_trade(schemas: TradeCreate = Depends(), user: User = Depends(cur_user)):
    trade_schema = schemas.model_dump()
    new_trade = await TradeRepository.add_trade_to_journal(trade_schema, user)
    return new_trade