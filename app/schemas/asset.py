from datetime import datetime

from pydantic import BaseModel, Field


class AssetIn(BaseModel):
    ticker: str = Field(min_length=1, max_length=10)
    quantity: float = Field(gt=0)
    average_price: float = Field(gt=0)


class AssetUpdate(BaseModel):
    quantity: float | None = Field(default=None, gt=0)
    average_price: float | None = Field(default=None, gt=0)


class AssetOut(BaseModel):
    id: int
    user_id: int
    ticker: str
    quantity: float
    average_price: float
    created_at: datetime

    class Config:
        from_attributes = True
