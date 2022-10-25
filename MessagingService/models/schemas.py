from datetime import datetime

from pydantic import BaseModel, Field


class AuthToken(BaseModel):
    user_id: str
    auth_token: str


class Message(BaseModel):
    sender: str
    receiver: str
    timestamp: datetime = Field(default_factory=datetime.now)
    content: str

    class Config:
        orm_mode = True


class DbMessage(Message):
    id: int
