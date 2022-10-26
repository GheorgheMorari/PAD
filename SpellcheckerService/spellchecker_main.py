import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from DiscoveryServiceUtils.discovery_comm import DiscoveryServiceComm
from SpellcheckerService.spellchecker_adapter import predict_misspelling

app = FastAPI()
SPELLCHECKER_SERVICE_HOST = "127.0.0.1"
SPELLCHECKER_SERVICE_PORT = 8082
SPELLCHECKER_SERVICE_NAME = "SpellcheckerService"
SPELLCHECKER_DISCOVERY = DiscoveryServiceComm(service_name=SPELLCHECKER_SERVICE_NAME,
                                              port=str(SPELLCHECKER_SERVICE_PORT))


class Message(BaseModel):
    text: str


@app.post("/")
def main(message: Message):
    return predict_misspelling(message.text)


@app.post("/status")
def status():
    return SPELLCHECKER_DISCOVERY.get_status_data()


if __name__ == "__main__":
    if not SPELLCHECKER_DISCOVERY.check_connection():
        raise Exception("Discovery service unavailable")

    if not SPELLCHECKER_DISCOVERY.register_force():
        raise Exception(f"Registration unsuccessful, Status code:{SPELLCHECKER_DISCOVERY.get_status_code()}")
    print("Registration successful")

    uvicorn.run(app, host=SPELLCHECKER_SERVICE_HOST, port=SPELLCHECKER_SERVICE_PORT)
