from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.database import Base, engine
from app.routes.assets import router as assets_router
from app.routes.portfolio import router as portfolio_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vault API")

app.include_router(auth_router)
app.include_router(assets_router)
app.include_router(portfolio_router)
