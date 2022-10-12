import requests
from flask import Flask, jsonify

app = Flask(__name__)

port = 7001
host = "127.0.0.1"
discovery_service_address = "http://127.0.0.1:6969/"

data = {
    "ServiceName": "testService",
    "Port": str(port),
    "Host": host
}


@app.route('/', methods=['GET', 'POST'])
def main():
    return jsonify(data)


if __name__ == "__main__":
    response = requests.post(discovery_service_address + "register", json=data)
    if response.status_code != 200:
        raise Exception("Request error")
    app.run(host=host, port=port)
