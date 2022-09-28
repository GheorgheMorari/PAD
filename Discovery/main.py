from flask import Flask,jsonify
import requests
addressList = ['http://127.0.0.1:7001/']
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    data = {}
    for address in addressList:
        response = requests.post(address)
        data[address] = response.json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)

