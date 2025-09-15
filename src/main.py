from fastapi import FastAPI
from src.auth.router import router as auth_router

app = FastAPI(
    title="Trade Journal"
)


#APIrouter connect
app.include_router(auth_router)
