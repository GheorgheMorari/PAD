import fastapi
import requests

AUTH_SERVICE_NAME = "AuthService"
AUTH_SERVICE_DEFAULT_ADDRESS = "http://127.0.0.1:8081/"


class AuthServiceComm:
    def __init__(self, auth_service_address=AUTH_SERVICE_DEFAULT_ADDRESS):
        self.auth_service_address = auth_service_address

        self.response_json = None
        self.user_id = None
        self.status_code = 0

    def connect(self, auth_service_address=AUTH_SERVICE_DEFAULT_ADDRESS) -> bool:
        self.auth_service_address = auth_service_address
        return self.check_connection()

    def check_connection(self) -> bool:
        try:
            response = requests.post(self.auth_service_address + "status")
        except:
            return False

        self.status_code = response.status_code
        try:
            self.response_json = response.json()
        except:
            self.response_json = None

        return response.status_code == 200

    def check_auth_token(self, request: fastapi.Request) -> bool:
        # header = {'Authorization': 'Bearer ' + bearer_token}
        headers = request.headers
        response = requests.post(self.auth_service_address + "api/users/me", headers=headers)
        try:
            self.response_json = response.json()
        except:
            self.response_json = None

        fail = (self.response_json is None) or ("user" not in self.response_json)
        if not fail:
            self.user_id = self.response_json["user"]["id"]

        self.status_code = response.status_code
        return (response.status_code == 200) or (not fail)
