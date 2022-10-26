from datetime import datetime

from pydantic import BaseModel, Field


class AuthToken(BaseModel):
    user_id: str
    auth_token: str


class InputMessage(BaseModel):
    receiver: str
    content: str


class Message(InputMessage):
    sender: str
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class DbMessage(Message):
    id: int
