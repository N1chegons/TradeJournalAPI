from datetime import datetime

import pytest
from pydantic import ValidationError

from src.trade.models import Direction
from src.trade.schemas import TradeCreate, TradeView, TradeViewAll

class TestTradeSchemas:
    # view schemas
    async def test_trade_view_valid(self):
        data_view = {
            "id": 1,
            "ticket": "BBC",
            "PnL": 10.0,
            "added_at": "2023-01-15T10:30:00"
        }
        trade = TradeView(**data_view)
        assert trade.id == 1
        assert trade.ticket == "BBC"
        assert trade.PnL == 10.0
        assert trade.added_at == "01.15.2023"
    async def test_trade_view_missing_field(self):
        data_view = {
            "id": 1,
            # "ticket": "BBC",
            "PnL": 10.0,
            "added_at": "2023-01-15T10:30:00"
        }
        with pytest.raises(ValidationError):
            TradeCreate(**data_view)
    async def test_trade_view_invalid_types(self):
        data_view = {
            "id": 1,
            "ticket": "BBC",
            "PnL": "10.2",
            "added_at": "2023-01-15T10:30:00"
        }
        with pytest.raises(ValidationError):
            TradeCreate(**data_view)

    # view all schemas
    async def test_trade_view_all_valid(self):
        data_view_all = {
            "id": 1,
            "ticket": "OXY",
            "direction": Direction.long,
            "entry_price": 500000.0,
            "exit_price": 510000.0,
            "quantity": 1.0,
            "PnL": 123.10,
            "added_at": "2023-01-15T10:30:00"
        }
        trade = TradeViewAll(**data_view_all)
        assert trade.id == 1
        assert trade.ticket == "OXY"
        assert trade.direction == Direction.long
        assert trade.entry_price == 500000.0
        assert trade.exit_price == 510000.0
        assert trade.PnL == 123.10
        assert trade.added_at == "01.15.2023"
    async def test_trade_view_all_missing_field(self):
        data_view_all = {
            "id": 1,
            # "ticket": "BTC",
            "direction": Direction.long,
            "entry_price": 500000.0,
            "exit_price": 510000.0,
            "quantity": 1.0,
            "PnL": 123.10,
            "added_at": "2023-01-15T10:30:00"
        }
        with pytest.raises(ValidationError):
            TradeCreate(**data_view_all)
    async def test_trade_view_all_invalid_types(self):
        data_view_all = {
            "id": 1,
            "ticket": "BTC",
            "direction": Direction.long,
            "entry_price": "hkhlljl",
            "exit_price": 510000.0,
            "quantity": 1.0,
            "PnL": 123.10,
            "added_at": "2023-01-15T10:30:00"
        }
        with pytest.raises(ValidationError):
            TradeViewAll(**data_view_all)

    # create schemas
    async def test_trade_create_valid(self):
        data_create = {
        "ticket": "BTC",
        "direction": Direction.long,
        "entry_price": 500000.0,
        "exit_price": 510000.0,
        "quantity": 1.0,
        }
        trade = TradeCreate(**data_create)

        assert trade.ticket == "BTC"
        assert trade.direction == Direction.long
        assert trade.exit_price == 510000.0
    async def test_trade_create_missing_field(self):
        data_create = {
            "ticket": "BTC",
            "direction": Direction.short,
            # "entry_price": 500000.0,
            "exit_price": 510000.0,
            "quantity": 1.0,
        }
        with pytest.raises(ValidationError):
            TradeCreate(**data_create)
    async def test_trade_create_invalid_types(self):
        data_create = {
            "ticket": "BTC",
            "direction": Direction.long,
            "entry_price": "invalid types field",
            "exit_price": 510000.0,
            "quantity": 1.0,
        }
        with pytest.raises(ValidationError):
            TradeCreate(**data_create)

    # test validator 'added_at'
    async def test_at_valid(self):
        data_view_all = {
            "id": 1,
            "ticket": "OXY",
            "direction": Direction.long,
            "entry_price": 500000.0,
            "exit_price": 510000.0,
            "quantity": 1.0,
            "PnL": 123.10,
            "added_at": "2023-01-15T10:30:00"
        }
        trade = TradeViewAll(**data_view_all)
        assert trade.added_at == "01.15.2023"
    async def test_at_valid_datetime(self):
        data_view_all = {
            "id": 1,
            "ticket": "OXY",
            "direction": Direction.long,
            "entry_price": 500000.0,
            "exit_price": 510000.0,
            "quantity": 1.0,
            "PnL": 123.10,
            "added_at": datetime(2024, 1, 15, 10, 30, 0)
        }
        trade = TradeViewAll(**data_view_all)
        assert trade.added_at == "01.15.2024"
    async def test_at_invalid(self):
        data_view_all = {
            "id": 1,
            "ticket": "OXY",
            "direction": Direction.long,
            "entry_price": 500000.0,
            "exit_price": 510000.0,
            "quantity": 1.0,
            "PnL": 123.10,
            "added_at": "isn't time"
        }
        with pytest.raises(ValidationError) as exc_info:
            trade = TradeViewAll(**data_view_all)

        assert "added_at" in str(exc_info.value)

