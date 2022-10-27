from datetime import datetime
from typing import List, Optional

import requests
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


toxicity_services = []
spellchecker_services = []
spellchecker_index = 0
toxicity_index = 0


def check_if_toxic(text: str, threshold: float = 0.5) -> bool:
    global toxicity_index
    global spellchecker_index
    if len(spellchecker_services) == 0:
        update()
        if len(spellchecker_services) == 0:
            raise HTTPException(status_code=500, detail="Could not connect with spellchecker service")
    if len(toxicity_services) == 0:
        update()
        if len(toxicity_services) == 0:
            raise HTTPException(status_code=500, detail="Could not connect with toxicity detection service")

    try:
        response = requests.post(spellchecker_services[spellchecker_index]["fullAddress"],
                                 json={"text": text})
    except requests.exceptions.RequestException:
        update()
        try:
            response = requests.post(spellchecker_services[spellchecker_index]["fullAddress"],
                                     json={"text": text})
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=500, detail="Could not connect with spellchecker service")

    spellchecker_index += 1
    spellchecker_index %= len(spellchecker_services)
    if not (response.status_code == 200):
        HTTPException(status_code=500, detail="Could not connect with spellchecker service")

    corrected_content = response.json()["corrected_content"]

    toxicity_index += 1
    toxicity_index %= len(toxicity_services)

    try:
        response = requests.post(toxicity_services[toxicity_index]["fullAddress"],
                                 json={"text": corrected_content})
    except requests.exceptions.RequestException:
        update()
        try:
            response = requests.post(toxicity_services[toxicity_index]["fullAddress"],
                                     json={"text": corrected_content})
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=500, detail="Could not connect with toxicity detection service")

    if not (response.status_code == 200):
        HTTPException(status_code=500, detail="Could not connect with toxicity detection service")
    toxicity = response.json()["toxic"]
    return toxicity >= threshold


@app.post("/send_message", response_model=schemas.DbMessage)
def create_message(request: Request, input_message: InputMessage, db: Session = Depends(get_db)):
    if MESSAGING_AUTH.check_auth_token(request):
        message = Message(sender=MESSAGING_AUTH.user_id, **input_message.dict())

        if check_if_toxic(message.content):
            raise HTTPException(status_code=403, detail="Message too toxic")

        return crud.create_message(db=db, message=message)
    raise HTTPException(status_code=403, detail="Invalid bearer auth token")


@app.post("/get_messages", response_model=List[schemas.DbMessage])
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


@app.post("/update")
def update():
    global toxicity_services
    global spellchecker_services
    toxicity_services = MESSAGING_DISCOVERY.get_service_addresses("ToxicityDetectionService")
    spellchecker_services = MESSAGING_DISCOVERY.get_service_addresses("SpellcheckerService")


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
    update()
    uvicorn.run(app, host=MESSAGING_SERVICE_HOST, port=MESSAGING_SERVICE_PORT)
