from datetime import datetime

from pydantic import BaseModel, Field


class NewsRequest(BaseModel):
    title: str = Field(min_length=5)
    content: str = Field(min_length=20)


class NewsPredictionResponse(BaseModel):
    id: int
    label: str
    confidence: float
    created_at: datetime


class AnalyticsSummary(BaseModel):
    total_predictions: int
    fake_count: int
    real_count: int
    fake_ratio: float
    average_confidence: float
