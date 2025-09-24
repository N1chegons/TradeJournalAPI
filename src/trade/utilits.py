from src.trade.models import Direction


def calculating_pnl(dir: Direction, entry_price: float, exit_price: float, quantity: float) -> float:
    if dir == Direction.long:
        pnl = (exit_price - entry_price) * quantity
    elif dir == Direction.short:
        pnl = (entry_price - exit_price) * quantity
    else:
        raise ValueError(f"Unknown trade direction: {dir}")
    return round(pnl, 2)