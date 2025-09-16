from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.trade.router import router as trade_router

app = FastAPI(
    title="Trade Journal"
)


#APIrouter connect
app.include_router(trade_router)
app.include_router(auth_router)
