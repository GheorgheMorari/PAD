from datetime import datetime
from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from AuthServiceUtils.auth_comm import AUTH_SERVICE_NAME, AuthServiceComm
from DiscoveryServiceUtils.discovery_comm import DiscoveryServiceComm
from MessagingService.models import schemas
from MessagingService.models.schemas import InputMessage, Message
from sql_app import crud, models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
MESSAGING_SERVICE_HOST = "127.0.0.1"
MESSAGING_SERVICE_PORT = 8069
MESSAGING_SERVICE_NAME = "MessagingService"
MESSAGING_DISCOVERY = DiscoveryServiceComm(service_name=MESSAGING_SERVICE_NAME, port=str(MESSAGING_SERVICE_PORT))
MESSAGING_AUTH = AuthServiceComm()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/messages", response_model=schemas.DbMessage)
def create_message(request: Request, input_message: InputMessage, db: Session = Depends(get_db)):
    if MESSAGING_AUTH.check_auth_token(request):
        message = Message(sender=MESSAGING_AUTH.user_id, **input_message.dict())
        return crud.create_message(db=db, message=message)
    raise HTTPException(status_code=403, detail="Invalid bearer auth token")


@app.get("/messages", response_model=List[schemas.DbMessage])
def get_message(request: Request, timestamp_from: datetime, timestamp_to: Optional[datetime] = None,
                db: Session = Depends(get_db)):
    if not MESSAGING_AUTH.check_auth_token(request):
        raise HTTPException(status_code=403, detail="Invalid bearer auth token")

    if timestamp_to is None:
        timestamp_to = datetime.now()
    messages = crud.get_messages_by_timestamp(db=db, participant_id=MESSAGING_AUTH.user_id,
                                              timestamp_from=timestamp_from,
                                              timestamp_to=timestamp_to)
    if len(messages) == 0:
        raise HTTPException(status_code=404, detail="No messages were not found")
    return messages


@app.post("/status")
def root():
    return MESSAGING_DISCOVERY.get_status_data()


if __name__ == "__main__":
    if not MESSAGING_DISCOVERY.check_connection():
        raise Exception("Discovery service unavailable")

    if not MESSAGING_DISCOVERY.register_force():
        raise Exception(f"Registration unsuccessful, Status code:{MESSAGING_DISCOVERY.get_status_code()}")
    print("Registration successful")

    auth_service_list = MESSAGING_DISCOVERY.get_service_addresses(AUTH_SERVICE_NAME)
    if len(auth_service_list) == 0:
        raise Exception("No auth service was registered")

    if not MESSAGING_AUTH.connect(auth_service_list[0]["fullAddress"]):
        raise Exception(f"Could not connect to auth service at:{auth_service_list[0]['fullAddress']}")
    print("Connection to auth service established")

    uvicorn.run(app, host=MESSAGING_SERVICE_HOST, port=MESSAGING_SERVICE_PORT)
