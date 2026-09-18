from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Action(str, Enum):
    REFUND = "REFUND"
    REPLACE = "REPLACE"
    REQUEST_PHOTOS = "REQUEST_PHOTOS"
    REQUEST_ORDER_DETAILS = "REQUEST_ORDER_DETAILS"
    DENY = "DENY"
    NEEDS_MORE_INFORMATION = "NEEDS_MORE_INFORMATION"
    ESCALATE = "ESCALATE"


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(RegisterRequest):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime


class TicketCreate(BaseModel):
    message: str = Field(min_length=10, max_length=5000)


class DecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    action: Action
    reason: str
    confidence: float = Field(ge=0, le=1)
    sources: list[str]
    created_at: datetime


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    message: str
    created_at: datetime
    decision: DecisionResponse | None
