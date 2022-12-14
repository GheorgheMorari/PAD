import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from ToxicityDetectionService.discovery_comm import DiscoveryServiceComm
from ToxicityDetectionService.toxicity_detection_adapter import predict_toxicity

app = FastAPI()
TOXICITY_DETECTION_SERVICE_HOST = os.getenv("TOXICITY_DETECTION_SERVICE_HOST", "127.0.0.1")
TOXICITY_DETECTION_SERVICE_PORT = os.getenv("PORT", 8085)
TOXICITY_DETECTION_SERVICE_NAME = "ToxicityDetectionService"
TOXICITY_DETECTION_DISCOVERY = DiscoveryServiceComm(service_name=TOXICITY_DETECTION_SERVICE_NAME,
                                                    port=str(TOXICITY_DETECTION_SERVICE_PORT),
                                                    host=TOXICITY_DETECTION_SERVICE_HOST)


class Message(BaseModel):
    text: str


@app.post("/")
def main(message: Message):
    return predict_toxicity(message.text)


@app.post("/status")
def status():
    return TOXICITY_DETECTION_DISCOVERY.get_status_data()


if not TOXICITY_DETECTION_DISCOVERY.check_connection():
    raise Exception("Discovery service unavailable")

if not TOXICITY_DETECTION_DISCOVERY.register_force():
    raise Exception(f"Registration unsuccessful, Status code:{TOXICITY_DETECTION_DISCOVERY.get_status_code()}")
print("Registration successful")
if __name__ == "__main__":
    uvicorn.run(app, host=TOXICITY_DETECTION_SERVICE_HOST, port=TOXICITY_DETECTION_SERVICE_PORT)
