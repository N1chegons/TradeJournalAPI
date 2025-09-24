from fastapi import APIRouter, Depends

from src.auth.models import User
from src.auth.router import cur_user
from src.trade.repository import TradeRepository
from src.trade.schemas import TradeCreate
from src.trade.utilits import calculating_pnl

router = APIRouter(
    prefix="/trade",
    tags=["Journal"]
)

# get
@router.get("/get_trades/", summary="Get trades journal")
async def get_trades(limit: int = 10, user: User = Depends(cur_user)):
    trades = await TradeRepository.get_all_trades_journal(user, limit)
    return trades

@router.get("/get_trade/{trade_id}/", summary="Get trades journal")
async def get_trade(trade_id: int, user: User = Depends(cur_user)):
    trades = await TradeRepository.get_one_trade_journal(trade_id, user)
    return trades


# post
@router.post("/add_trade/", description="Write a ticket in XXX format.")
async def add_trade(schemas: TradeCreate = Depends(), user: User = Depends(cur_user)):
    trade_schema = schemas.model_dump()
    pnl = calculating_pnl(
        dir=schemas.direction,
        entry_price=schemas.entry_price,
        exit_price=schemas.exit_price,
        quantity=schemas.quantity
    )
    new_trade = await TradeRepository.add_trade_to_journal(trade_schema, user, pnl)
    return new_trade

# patch
@router.put("/update_trade/{trade_id}/", summary="Update trade with ID.")
async def update_trade(trade_id: int, schemas: TradeCreate = Depends(),  user: User = Depends(cur_user)):
    # new PnL value
    pnl = calculating_pnl(
        dir=schemas.direction,
        entry_price=schemas.entry_price,
        exit_price=schemas.exit_price,
        quantity=schemas.quantity
    )

    updated_trade = await TradeRepository.update_trade_in_journal(trade_id, schemas, pnl, user)
    return updated_trade
