from unittest.mock import patch, AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


from src.auth.models import User
from src.trade.repository import TradeRepository



class TestTradeRepository:
    async def test_get_all_trades_journal(self, mock_user):
        with pytest.raises(HTTPException) as exc:
            await TradeRepository.get_all_trades_journal(mock_user, limit=10)
        assert exc.value.status_code == 404
        assert "There is not a single trade." in exc.value.detail
