import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from AuthService.app.config import settings
from AuthService.app.routers import auth, user
from AuthService.auth_comm import AUTH_SERVICE_NAME
from AuthService.discovery_comm import DiscoveryServiceComm

app = FastAPI()
AUTH_SERVICE_HOST = os.getenv("AUTH_SERVICE_HOST", "127.0.0.1")
AUTH_SERVICE_PORT = 8081
AUTH_DISCOVERY = DiscoveryServiceComm(service_name=AUTH_SERVICE_NAME, port=str(AUTH_SERVICE_PORT),
                                      host=AUTH_SERVICE_HOST)

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
    return AUTH_DISCOVERY.get_status_data()


if not AUTH_DISCOVERY.check_connection():
    raise Exception("Discovery service unavailable")

if not AUTH_DISCOVERY.register_force():
    raise Exception(f"Registration unsuccessful, Status code:{AUTH_DISCOVERY.get_status_code()}")
print("Registration successful")

if __name__ == "__main__":
    uvicorn.run(app, host=AUTH_SERVICE_HOST, port=AUTH_SERVICE_PORT)
