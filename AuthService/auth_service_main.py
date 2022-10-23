import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, user

app = FastAPI()
auth_service_host = "127.0.0.1"
auth_service_port = 8081
discovery_service_address = "http://127.0.0.1:6969/"

status_data = {
    "ServiceName": "AuthService",
    "Port": str(auth_service_port),
    "Host": auth_service_host
}

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')


@app.post("/status")
def root():
    return status_data


if __name__ == "__main__":
    response = requests.post(discovery_service_address + "register", json={"ServiceName": "AuthService",
                                                                           "Port": str(auth_service_port),
                                                                           "Host": auth_service_host})
    if response.status_code != 200:
        raise Exception("Discovery service unavailable")
    print("Registration successful")
    uvicorn.run(app, host=auth_service_host, port=auth_service_port)
