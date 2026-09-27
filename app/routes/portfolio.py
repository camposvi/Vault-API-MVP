import os

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.database import get_db
from app.models.asset import Asset
from app.models.user import User
from app.schemas.portfolio import PortfolioSummary

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

TICKER_URL = os.getenv("TICKER_URL", "http://localhost:8001")


@router.get("/summary", response_model=PortfolioSummary)
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assets = db.query(Asset).filter(Asset.user_id == current_user.id).all()
    if not assets:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No assets found for this user")

    payload = {
        "assets": [
            {
                "ticker": asset.ticker,
                "quantity": asset.quantity,
                "average_price": asset.average_price,
            }
            for asset in assets
        ]
    }

    try:
        response = httpx.post(f"{TICKER_URL}/portfolio/calculate", json=payload, timeout=10)
    except httpx.TimeoutException:
        raise HTTPException(status.HTTP_504_GATEWAY_TIMEOUT, "Ticker API timed out")
    except httpx.HTTPError:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Ticker API unavailable")

    if response.status_code >= 400:
        raise HTTPException(response.status_code, response.text)

    return response.json()
