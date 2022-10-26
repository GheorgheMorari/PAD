import threading
import time
from typing import List, Optional

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from requests import Response

from Discovery.domain.models import Service, RegistrationService
from DiscoveryServiceUtils.discovery_comm import DEFAULT_DISCOVERY_SERVICE_PORT, DEFAULT_DISCOVERY_SERVICE_HOST

# Constants
DISCOVERY_HOST = DEFAULT_DISCOVERY_SERVICE_HOST
DISCOVERY_PORT = DEFAULT_DISCOVERY_SERVICE_PORT
RUN_CHECK_ROUTINE = False
CHECK_ROUTINE_DELAY_SECONDS = 5
STATUS_ENTRYPOINT_NAME = "status"

# Global variables
services: List[Service] = []
app = FastAPI()


def send_post(address) -> Optional[Response]:
    try:
        return requests.post(address)
    except:
        return None


def check_routine():
    while True:
        check()
        time.sleep(CHECK_ROUTINE_DELAY_SECONDS)


@app.post("/")
def main():
    return services


@app.post('/check')
def check():  # Check if the services are still running by pinging the status entrypoint
    responses = [send_post(service.fullAddress + STATUS_ENTRYPOINT_NAME) for service in
                 services]  # Send all requests one after another

    offsets = 0
    for i in range(len(responses)):  # Remove the services that did not connect or did not return 200
        if not responses[i] or responses[i].status_code != 200:
            print("removed service", services[i - offsets].serviceName, " at address: ",
                  services[i - offsets].fullAddress)
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
def delete(request: Request, registration_service: RegistrationService):
    service = Service(
        fullAddress=f"http://{request.client.host if not registration_service.Host else registration_service.Host}:{registration_service.Port}/",
        serviceName=registration_service.ServiceName)
    try:
        services.remove(service)
    except:
        raise HTTPException(status_code=404)  # Service doesn't exist


if __name__ == "__main__":
    if RUN_CHECK_ROUTINE:
        routine = threading.Thread(target=check_routine)
        routine.start()
    uvicorn.run(app, host=DISCOVERY_HOST, port=DISCOVERY_PORT)
