import pytest
from src.trade.models import Trade, Direction


def test_as():
    assert 1 == 1

# class TestTradeService:
#     def test_trade_creation(self):
#         # Test create model Trade
#         trade = Trade(
#             ticket="AAPL",
#             direction=Direction.long,
#             entry_price=150.0,
#             exit_price=155.0,
#             quantity=10,
#             PnL=50.0,
#         )
#         assert trade.ticket == "AAPL"
#         assert trade.direction == Direction.long
#         assert trade.PnL == 50.0