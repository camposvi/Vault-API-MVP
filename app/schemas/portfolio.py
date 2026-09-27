from pydantic import BaseModel


class AssetPosition(BaseModel):
    ticker: str
    quantity: float
    average_price: float
    current_price: float
    current_value: float
    profit_percentage: float


class PortfolioSummary(BaseModel):
    total_invested: float
    total_current_value: float
    total_profit_percentage: float
    positions: list[AssetPosition]
