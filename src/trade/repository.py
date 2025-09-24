from fastapi import HTTPException
from sqlalchemy import select, insert, update

from src.auth.models import User
from src.database import async_session
from src.trade.models import Trade
from src.trade.schemas import TradeView, TradeViewAll


class TradeRepository:
    # get
    @classmethod
    async def get_all_trades_journal(cls, user: User, limit: int):
        async with async_session() as session:
            query = select(Trade).filter_by(user_id=user.id).limit(limit)
            result = await session.execute(query)
            trades = result.unique().scalars().all()
            trades_list = [TradeView.model_validate(p) for p in trades]
            if trades_list:
                return {
                    "status": 200,
                    "trades": trades_list
                }
            else:
                raise HTTPException(
                    status_code=404,
                    detail="There is not a single trade."
                )

    @classmethod
    async def get_one_trade_journal(cls, trade_id: int, user: User):
        async with async_session() as session:
            query = select(Trade).filter_by(user_id=user.id, id=trade_id)
            result = await session.execute(query)
            trades = result.unique().scalars().all()
            trades_list = [TradeViewAll.model_validate(p) for p in trades]
            if trades_list:
                return {
                    "status": 200,
                    "trades": trades_list
                }
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Trade by id {trade_id} not found."
                )

    # post
    @classmethod
    async def add_trade_to_journal(cls, values: dict, user: User, pnl_count: float):
        async with async_session() as session:
            stmt = insert(Trade).values(**values, user_id=user.id, PnL=pnl_count).returning(Trade)
            try:
                add_trade = await session.execute(stmt)
                await session.commit()
                return {
                    "status": 200,
                    "message": "New trade added"
                }
            except:
                raise HTTPException(
                    status_code=500,
                    detail="Unknown error."
                )

    # put
    @classmethod
    async def update_trade_in_journal(cls, trade_id: int,  update_data: dict, pnl: float, user: User):
        async with async_session() as session:
            # noinspection PyUnresolvedReferences
            update_data = update_data.model_dump()
            update_data["PnL"] = pnl
            stmt = (
                update(Trade)
                .filter_by(id=trade_id, user_id=user.id)
                .values(**update_data)
                .returning(Trade)
            )
            try:
                await session.execute(stmt)
                await session.commit()
                return {
                    "status": 200,
                    "message": "The trade has been updated"
                }
            except:
                raise HTTPException(
                    status_code=500,
                    detail="Unknown error."
                )

