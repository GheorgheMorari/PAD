from flask import Flask, jsonify, request
import requests

addressList = []
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    data = {}
    for address in addressList:
        # make a post request and save the response
        response = requests.post(address)
        data[address] = response.json()
    return jsonify(data)


@app.route('/register', methods=['POST'])
def register():
    currentRequest = request
    remote_addr = currentRequest.remote_addr
    port = currentRequest.json["port"]  # TODO return status bad request 4hundredsumthin if request does not have a json
    full_address = "http://" + remote_addr + ":" + str(port) + "/"
    addressList.append(full_address)
    return "Ok"

@app.route('/delete', methods=['POST'])
def delete():
    currentRequest = request
    remote_addr = currentRequest.remote_addr
    port = currentRequest.json["port"]
    full_address = "http://" + remote_addr + ":" + str(port) + "/"
    addressList.remove(full_address)
    return "Removed"

# TODO make the opposite of register that deletes the address from the addressList

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)
