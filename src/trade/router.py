from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from fastapi import Response
from fastapi.params import Query, Depends

from src.auth.models import User
from src.auth.router import cur_user
from src.trade.repository import TradeRepository, ExportService
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
    trade = await TradeRepository.get_one_trade_journal(trade_id, user)
    return trade

@router.get("/search_filter_trades/", summary="Get trades with filters")
async def get_trades_filters(
        ticket: Optional[str] = Query(None),
        direction: Optional[str] = Query(None, description="Long/Short"),
        date_from: Optional[datetime] = Query(None),
        date_to: Optional[datetime] = Query(None),
        min_pnl: Optional[float] = Query(None),
        max_pnl: Optional[float] = Query(None),
        sort_by: str = Query("newest", description="newest, oldest, pnl_high, pnl_low"),
        user: User = Depends(cur_user),
        limit: int = 50,
):
    trades = await TradeRepository.get_more_trade_filter_journal(
        ticket = ticket,
        direction = direction,
        date_from = date_from,
        date_to = date_to,
        min_pnl = min_pnl,
        max_pnl = max_pnl,
        sort_by = sort_by,
        limit = limit,
        user = user,
    )
    return trades

@router.get("/import_trades_csv/")
async def get_all_trades_csv(user: User = Depends(cur_user)):
    csv_data, filename = await ExportService.get_all_trades_CSV(user)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition":
                f"attachment; filename={filename}",
            "Content-Type":  "text/csv; charset=utf-8"
        }
    )

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

# put
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

# delete
@router.delete("/delete_trade/{trade_id}/", summary="Delete trade with ID")
async def delete_trade(trade_id: int, user: User = Depends(cur_user)):
    del_trade = await TradeRepository.delete_trade_in_journal(trade_id, user)
    return del_trade

@router.delete("/delete_trades/", summary="Delete all trades")
async def delete_trade(user: User = Depends(cur_user)):
    del_trades = await TradeRepository.delete_all_trades_in_journal(user)
    return del_trades