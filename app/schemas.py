
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional


# ---------- Auth ----------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
    email: EmailStr
    roles: List[str]


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    user_id: int
    roles: List[str]


# ---------- Series ----------

class SeriesBase(BaseModel):
    series_id: int
    name: str
    num_episodes: int
    release_date: date
    language_code: str
    origin_country: str


class SeriesOut(SeriesBase):
    pass


# ---------- Feedback ----------

class FeedbackCreate(BaseModel):
    series_id: int
    account_id: int
    rating: int
    feedback_text: Optional[str] = None


class FeedbackOut(BaseModel):
    account_id: int
    rating: int
    feedback_text: Optional[str]
    feedback_date: date


# ---------- Contracts ----------

class ContractOut(BaseModel):
    contract_id: int
    series_id: int
    per_episode_charge: float
    status: str
    contract_start_date: date
    contract_end_date: date
