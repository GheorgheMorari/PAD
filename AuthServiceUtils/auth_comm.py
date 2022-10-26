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

    def check_auth_token(self, bearer_token: str) -> bool:
        header = {'Authorization': 'Bearer ' + bearer_token}
        response = requests.post(self.auth_service_address + "api/users/me", headers=header)
        try:
            self.response_json = response.json()
        except:
            self.response_json = None

        if self.response_json is not None:
            self.user_id = self.response_json["user"]["id"]

        self.status_code = response.status_code
        return (response.status_code == 200) or (self.response_json is None)
