from typing import Optional

from pydantic import BaseModel


class Service(BaseModel):
    serviceName: str
    fullAddress: str


class RegistrationService(BaseModel):
    Port: str
    Host: Optional[str]
    ServiceName: str
