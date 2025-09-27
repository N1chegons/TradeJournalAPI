from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete

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

    @classmethod
    async def get_more_trade_filter_journal(cls,limit: int,  user: User, **filters):
        async with async_session() as session:
            query = select(Trade).where(Trade.user_id == user.id)
            if filters.get('ticket'):
                query = query.where(Trade.ticket.ilike(f"%{filters['ticket']}%"))

            if filters.get('direction'):
                query = query.where(Trade.direction == filters['direction'])

            if filters.get('date_from'):
                query = query.where(Trade.added_at >= filters['date_from'])
            if filters.get('date_to'):
                query = query.where(Trade.added_at <= filters['date_to'])

            if filters.get('min_pnl') is not None:
                query = query.where(Trade.PnL >= filters['min_pnl'])
            if filters.get('max_pnl') is not None:
                query = query.where(Trade.PnL <= filters['max_pnl'])

            sort_options = {
                "newest": Trade.added_at.desc(),
                "oldest": Trade.added_at.asc(),
                "pnl_high": Trade.PnL.desc(),
                "pnl_low": Trade.PnL.asc()
            }
            query = query.order_by(sort_options.get(filters.get('sort_by', 'newest')))

            query = query.limit(filters.get('limit', limit))
            try:
                result = await session.execute(query)
                trades = result.scalars().all()
                trades_list = [TradeViewAll.model_validate(p) for p in trades]
                if trades_list:
                    return trades_list
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="There is not a single trade."
                    )
            except:
                raise HTTPException(
                    status_code=500,
                    detail="Please check a field.Unfounded error"
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

    # delete
    @classmethod
    async def delete_trade_in_journal(cls, trade_id: int, user: User):
        async with async_session() as session:
            query = delete(Trade).filter_by(id=trade_id)
            trade = await session.get(Trade, trade_id)

            if not trade or trade.user_id != user.id:
                raise HTTPException(
                    status_code=404,
                    detail=f"Trade with id {trade_id} not found."
                )

            try:
                await session.execute(query)
                await session.commit()
                return {
                    "status": 200,
                    "message": f"The trade with id={trade_id} has deleted",
                }
            except:
                raise HTTPException(
                    status_code=500,
                    detail="Unknown error."
                )

    @classmethod
    async def delete_all_trades_in_journal(cls, user: User):
        async with async_session() as session:
            query = delete(Trade).filter_by(user_id=user.id)
            try:
                await session.execute(query)
                await session.commit()
                return {
                    "status": 200,
                    "message": f"All trades has deleted",
                }
            except:
                raise HTTPException(
                    status_code=500,
                    detail="Unknown error."
                )

