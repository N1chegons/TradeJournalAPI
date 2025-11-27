import pytest

from src.trade.models import Direction
from src.trade.utilits import calculating_pnl


class TestCalculatingPnL:
    # long
    async def test_calculating_pnl_long_win(self):
        result = calculating_pnl(Direction.long, 24500.75, 25120.30, 2.5)
        assert result == 1548.87
    async def test_calculating_pnl_long_loose(self):
        result = calculating_pnl(Direction.long, 1022.20, 1000.24, 41.5)
        assert result == -911.34
    # short
    async def test_calculating_pnl_short_win(self):
        result = calculating_pnl(Direction.short, 1800.50, 1755.25, 15)
        assert result == 678.75
    async def test_calculating_pnl_short_loose(self):
        result = calculating_pnl(Direction.short, 32500.80, 33100.40, 100)
        assert result == -59960
    # Invalid direction
    async def test_calculating_pnl_invalid_field(self):
        with pytest.raises(ValueError, match="Unknown trade direction"):
            result = calculating_pnl("TOP", 24500.75, 25120.30, 2.5)

