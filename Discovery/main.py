import time
from typing import List, Optional

import ray
import requests
import uvicorn as uvicorn
from fastapi import Request, FastAPI, HTTPException
from requests import Response

from Discovery.domain.models import Service, RegistrationService

ray.init()
services: List[Service] = []
app = FastAPI()

RUN_CHECK_ROUTINE = False


@ray.remote
def send_post(address) -> Optional[Response]:
    try:
        return requests.post(address)
    except:
        return None


@ray.remote
def check_routine():
    while True:
        check()
        time.sleep(1)


@app.get('/check')
def check():
    pool = [send_post.remote(service.fullAddress) for service in services]  # Send all requests asynchronously
    responses = ray.get(pool)  # Block thread until all requests either time out or receive response

    offsets = 0
    for i in range(len(responses)):  # Remove the services that did not connect or did not return 200
        if not responses[i] or responses[i].status_code != 200:
            del services[i - offsets]
            offsets += 1

    return services


@app.post('/register')
def register(request: Request, registration_service: RegistrationService):
    service = Service(
        fullAddress=f"http://{request.client.host if not registration_service.Host else registration_service.Host}:{registration_service.Port}/",
        serviceName=registration_service.ServiceName)
    if service in services:
        raise HTTPException(status_code=409)  # Service already exists
    else:
        services.append(service)


@app.post('/delete')
def register(request: Request, registration_service: RegistrationService):
    service = Service(
        fullAddress=f"http://{request.client.host if not registration_service.Host else registration_service.Host}:{registration_service.Port}/",
        serviceName=registration_service.ServiceName)
    try:
        services.remove(service)
    except:
        raise HTTPException(status_code=404)  # Service doesn't exist


if __name__ == "__main__":
    if RUN_CHECK_ROUTINE:
        check_routine.remote()
    uvicorn.run(app, host="0.0.0.0", port=6969)
