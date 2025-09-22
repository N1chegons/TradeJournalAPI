from fastapi import HTTPException
from sqlalchemy import select, insert, update

from src.auth.models import User
from src.database import async_session
from src.trade.models import Trade
from src.trade.schemas import TradeView, TradeUpdate
from src.trade.utilits import calculating_pnl


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

    @classmethod
    async def update_trade(
            cls,
            trade_id: int,
            user_id: int,
            update_data: TradeUpdate
    ) -> Trade | None:

        async with async_session() as session:
            trade = await session.get(Trade, trade_id)
            if not trade or trade.user_id != user_id:
                raise HTTPException(
                    status_code=404,
                    detail="Not Found."
                )
            update_values = update_data.model_dump(exclude_unset=True)


            if any(key in update_values for key in ['entry_price', 'exit_price', 'quantity', 'direction']):
                entry_price = update_values.get('entry_price', trade.entry_price)
                exit_price = update_values.get('exit_price', trade.exit_price)
                quantity = update_values.get('quantity', trade.quantity)
                direction = update_values.get('direction', trade.direction)

                update_values['pnl'] = calculating_pnl(direction, entry_price, exit_price, quantity)

            if not update_values:
                return trade

            stmt = (
                update(Trade)
                .where(Trade.id == trade_id, Trade.user_id == user_id)  # Двойная проверка
                .values(**update_values)
                .returning(Trade)
            )

            result = await session.execute(stmt)
            await session.commit()

            updated_trade = result.scalar_one_or_none()
            if updated_trade:
                await session.refresh(updated_trade)
            return updated_trade
