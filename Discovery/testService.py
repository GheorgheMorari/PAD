from flask import Flask, jsonify
import requests

app = Flask(__name__)
port = 7001

discovery_service_address = "http://127.0.0.1:6969/"

data = {
    "Status": "running",
    "Name": "testService",
}


@app.route('/', methods=['GET', 'POST'])
def main():
    return jsonify(data)


if __name__ == "__main__":
    response = requests.post(discovery_service_address + "register", json={"port": port})
    if response.status_code != 200:
        raise Exception("Request error")
    app.run(host='0.0.0.0', port=port)
