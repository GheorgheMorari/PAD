from flask import Flask,jsonify,request
import requests
addressList = ['http://127.0.0.1:7001/']
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    data = {}
    for address in addressList:
        #make a post request and save the response
        response = requests.post(address)
        data[address] = response.json()
    return jsonify(data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    currentRequest = request
    remote_addr = currentRequest.remote_addr
    port = currentRequest.json()["port"]

    print(currentRequest)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)

