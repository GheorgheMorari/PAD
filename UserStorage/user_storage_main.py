import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, user

app = FastAPI()
user_storage_host = "127.0.0.1"
user_storage_port = 8081
discovery_service_address = "http://127.0.0.1:6969/"

status_data = {
    "ServiceName": "UserStorage",
    "Port": str(user_storage_port),
    "Host": user_storage_host
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
    response = requests.post(discovery_service_address + "register", json={"ServiceName": "UserStorage",
                                                                           "Port": str(user_storage_port),
                                                                           "Host": user_storage_host})
    if response.status_code != 200:
        raise Exception("Discovery service unavailable")
    print("Registration successful")
    uvicorn.run(app, host=user_storage_host, port=user_storage_port)
