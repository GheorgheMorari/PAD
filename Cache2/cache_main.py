import json
import os
import threading
import time
from datetime import datetime, timedelta
from typing import List

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

from Cache.discovery_comm import DiscoveryServiceComm
from Cache.schemas import DbMessage

app = FastAPI()
CACHE_STORAGE_TIME = timedelta(minutes=1)
CACHE_DELETE_ROUTINE_DELAY_SECONDS = 20
CACHE_SERVICE_HOST = os.getenv("CACHE_SERVICE_HOST", "127.0.0.1")
CACHE_SERVICE_PORT = 8078
CACHE_SERVICE_NAME = "CacheService"
CACHE_DISCOVERY = DiscoveryServiceComm(service_name=CACHE_SERVICE_NAME,
                                       port=str(CACHE_SERVICE_PORT), host=CACHE_SERVICE_HOST)


class CacheMessage(DbMessage):
    expire_time: datetime

    def __eq__(self, other):
        if type(other) == CacheQuery:
            return (self.timestamp >= other.timestamp_from) and (self.timestamp <= other.timestamp_to) and (
                    (self.sender == other.participant) or (self.receiver == other.participant))
        if type(other) == datetime:
            return self.expire_time >= other


class CacheQuery(BaseModel):
    timestamp_from: datetime
    timestamp_to: datetime
    participant: str


cache_storage: List[CacheMessage] = []


@app.post("/")
async def main(request: Request):
    body = await request.body()
    command, object_str = body.decode(encoding='utf-8').split("<__-__>")
    if command == "store":
        object_dict = json.loads(object_str)
        cache_storage.append(CacheMessage(expire_time=datetime.now() + CACHE_STORAGE_TIME, **object_dict))
        return "OK"
    elif command == "get":
        object_dict = json.loads(object_str)
        query = CacheQuery(**object_dict)
        return list(filter(lambda x: x == query, cache_storage))

    raise HTTPException(status_code=400, detail="Invalid command")


def delete_routine():
    global cache_storage
    while True:
        time.sleep(CACHE_DELETE_ROUTINE_DELAY_SECONDS)
        now = datetime.now()
        cache_storage = list(filter(lambda x: x == now, cache_storage))


@app.post("/status")
def status():
    return CACHE_DISCOVERY.get_status_data()


if not CACHE_DISCOVERY.check_connection():
    raise Exception("Discovery service unavailable")

if not CACHE_DISCOVERY.register_force():
    raise Exception(f"Registration unsuccessful, Status code:{CACHE_DISCOVERY.get_status_code()}")
print("Registration successful")
routine = threading.Thread(target=delete_routine)
routine.daemon = True
routine.start()
if __name__ == "__main__":

    uvicorn.run(app, host=CACHE_SERVICE_HOST, port=CACHE_SERVICE_PORT)
