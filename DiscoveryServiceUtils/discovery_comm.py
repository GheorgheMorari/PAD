from typing import Optional

import requests


class DiscoveryServiceComm:
    def __init__(self, port: str, service_name: str, host: Optional[str] = None,
                 discovery_service_address="http://127.0.0.1:6969/"):
        self.host = host
        self.port = port
        self.discovery_service_address = discovery_service_address
        self.status_data = {
            "ServiceName": service_name,
            "Port": port,
        }
        if host:
            self.status_data["Host"] = host

        self.status_code = 0

    def check_connection(self) -> bool:
        response = requests.post(self.discovery_service_address)
        self.status_code = response.status_code
        return response.status_code == 200

    def register(self) -> bool:
        response = requests.post(self.discovery_service_address + "register", json=self.status_data)
        self.status_code = response.status_code
        return response.status_code == 200

    def delete(self):
        response = requests.post(self.discovery_service_address + "delete", json=self.status_data)
        self.status_code = response.status_code
        return response.status_code == 200

    def register_force(self) -> bool:
        if not self.register():

            if not self.delete():  # Delete entry
                return False

            if not self.register():  # Register once again
                return False

        return True

    def get_status_code(self) -> int:
        return self.status_code

    def get_status_data(self) -> dict:
        return self.status_data
