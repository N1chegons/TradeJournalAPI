from fastapi import HTTPException
from sqlalchemy import select, insert

from src.auth.models import User
from src.database import async_session
from src.trade.models import Trade
from src.trade.schemas import TradeView


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
                return {
                    "status": 404,
                    "message": "There is not a single trade."
                }

    # post
    @classmethod
    async def add_trade_to_journal(cls, values: dict, user: User):
        async with async_session() as session:
            stmt = insert(Trade).values(**values, user_id=user.id).returning(Trade)
            try:
                add_trade = await session.execute(stmt)
                await session.commit()
                return {
                    "status": 200,
                    "message": "New trade added"
                }
            except:
                raise HTTPException(
                    status_code=204,
                    detail="Unknown error"
                )