import json
from datetime import datetime
from typing import List, Optional

import requests
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from AuthServiceUtils.auth_comm import AUTH_SERVICE_NAME, AuthServiceComm
from DiscoveryServiceUtils.discovery_comm import DiscoveryServiceComm
from DistributedServiceUtils.distributed_service_comm import DistributedServiceComm
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
cache_services = []

toxicity_comm = DistributedServiceComm(toxicity_services)
spellchecker_comm = DistributedServiceComm(spellchecker_services)


def high_availability_request_comm(comm: DistributedServiceComm, json_data: dict) -> Optional[requests.Response]:
    response = None
    try:
        response = comm.send_post(json_data=json_data)
    except requests.exceptions.RequestException:
        update()  # Force update toxicity_services
        try:
            response = comm.send_post(json_data=json_data)
        except requests.exceptions.RequestException:
            return None

    return response


def check_if_toxic(text: str, threshold: float = 0.5) -> bool:
    response = high_availability_request_comm(spellchecker_comm, json_data={"text": text})
    if response is None or response.status_code != 200:
        raise HTTPException(status_code=500, detail="Could not connect with spellchecker service")

    corrected_content = response.json()["corrected_content"]
    response = high_availability_request_comm(toxicity_comm, json_data={"text": corrected_content})

    if response is None or response.status_code != 200:
        HTTPException(status_code=500, detail="Could not connect with toxicity detection service")
    toxicity = response.json()["toxic"]

    return toxicity >= threshold


@app.post("/send_message", response_model=schemas.DbMessage)
def create_message(request: Request, input_message: InputMessage, db: Session = Depends(get_db)):
    if MESSAGING_AUTH.check_auth_token(request):
        message = Message(sender=MESSAGING_AUTH.user_id, **input_message.dict())

        if check_if_toxic(message.content):
            raise HTTPException(status_code=403, detail="Message too toxic")
        db_message = crud.create_message(db=db, message=message)
        store_message_to_cache(schemas.DbMessage(id=db_message.id, **message.dict()))
        return db_message
    raise HTTPException(status_code=403, detail="Invalid bearer auth token")


@app.post("/get_messages", response_model=List[schemas.DbMessage])
def get_message(request: Request, timestamp_from: datetime, timestamp_to: Optional[datetime] = None,
                db: Session = Depends(get_db)):
    if not MESSAGING_AUTH.check_auth_token(request):
        raise HTTPException(status_code=403, detail="Invalid bearer auth token")

    if timestamp_to is None:
        timestamp_to = datetime.now()

    # Check cache
    cache_messages = get_messages_from_cache(participant=MESSAGING_AUTH.user_id, timestamp_from=timestamp_from,
                                             timestamp_to=timestamp_to)
    if len(cache_messages) != 0:
        return cache_messages

    messages = crud.get_messages_by_timestamp(db=db, participant_id=MESSAGING_AUTH.user_id,
                                              timestamp_from=timestamp_from,
                                              timestamp_to=timestamp_to)
    if len(messages) == 0:
        raise HTTPException(status_code=404, detail="No messages were not found")
    return messages


@app.post("/status")
def root():
    return MESSAGING_DISCOVERY.get_status_data()


def update():
    toxicity_services[:] = [x['fullAddress'] for x in
                            MESSAGING_DISCOVERY.get_service_addresses("ToxicityDetectionService")]
    spellchecker_services[:] = [x['fullAddress'] for x in
                                MESSAGING_DISCOVERY.get_service_addresses("SpellcheckerService")]
    cache_services[:] = [x['fullAddress'] for x in MESSAGING_DISCOVERY.get_service_addresses("CacheService")]


def store_message_to_cache(message: schemas.DbMessage):
    if len(cache_services) == 0:
        update()
        if len(cache_services) == 0:
            return

    try:
        response = requests.post(cache_services[0]["fullAddress"],
                                 data=f'store<__-__>{json.dumps(message.dict(), default=str)}')
    except requests.exceptions.RequestException:
        update()
        try:
            response = requests.post(cache_services[0]["fullAddress"],
                                     data=f'store<__-__>{json.dumps(message.dict(), default=str)}')
        except requests.exceptions.RequestException:
            return
    #
    # if not (response.status_code == 200):
    #     return


def get_messages_from_cache(participant: str, timestamp_from: datetime, timestamp_to: datetime) -> List[
    schemas.DbMessage]:
    if len(cache_services) == 0:
        update()
        if len(cache_services) == 0:
            return []
            # raise HTTPException(status_code=500, detail="Could not connect with cache service")
    try:
        response = requests.post(cache_services[0]["fullAddress"],
                                 data=f'get<__-__>{json.dumps({"participant": participant, "timestamp_from": str(timestamp_from), "timestamp_to": str(timestamp_to)})}')
    except requests.exceptions.RequestException:
        update()
        try:
            response = requests.post(cache_services[0]["fullAddress"],
                                     data=f'get<__-__>{json.dumps({"participant": participant, "timestamp_from": str(timestamp_from), "timestamp_to": str(timestamp_to)})}')
        except requests.exceptions.RequestException:
            return []

    if not (response.status_code == 200):
        return []
    response_dict_list = response.json()

    ret = []
    for response_dict in response_dict_list:
        response_dict.pop("expire_time", None)
        ret.append(schemas.DbMessage(**response_dict))

    return ret


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
