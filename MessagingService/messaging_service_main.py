from datetime import datetime
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from DiscoveryServiceUtils.discovery_comm import DiscoveryServiceComm
from MessagingService.models import schemas
from sql_app import crud, models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
MESSAGING_SERVICE_HOST = "127.0.0.1"
MESSAGING_SERVICE_PORT = 8069
MESSAGING_SERVICE_NAME = "MessagingService"
MESSAGING_DISCOVERY = DiscoveryServiceComm(service_name=MESSAGING_SERVICE_NAME, port=str(MESSAGING_SERVICE_PORT))


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/messages", response_model=schemas.DbMessage)
def create_message(message: schemas.Message, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)


@app.get("/messages", response_model=schemas.DbMessage)
def get_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.get_message(db=db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message


@app.get("/messages/timestamp", response_model=List[schemas.DbMessage])
def get_message(participant_id: str, timestamp_from: datetime, timestamp_to: datetime = datetime.now(),
                db: Session = Depends(get_db)):
    messages = crud.get_messages_by_timestamp(db=db, participant_id=participant_id, timestamp_from=timestamp_from,
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
    uvicorn.run(app, host=MESSAGING_SERVICE_HOST, port=MESSAGING_SERVICE_PORT)
