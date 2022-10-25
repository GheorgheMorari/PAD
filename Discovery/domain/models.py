from typing import Optional, Union

from pydantic import BaseModel


class Service(BaseModel):
    serviceName: str
    fullAddress: str


class RegistrationService(BaseModel):
    Port: str
    Host: Optional[str]
    ServiceName: str
