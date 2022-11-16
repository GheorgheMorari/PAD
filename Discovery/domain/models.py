from typing import Optional, List

from pydantic import BaseModel


class Service(BaseModel):
    serviceName: str
    fullAddress: str


class RegistrationService(BaseModel):
    Port: str
    Host: Optional[str]
    ServiceName: str


class SubscriptionService(BaseModel):
    Port: str
    Host: Optional[str]
    ServiceNames: List[str]
