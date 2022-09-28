from flask import Flask,jsonify

app = Flask(__name__)
data = {
    "Status": "running",
    "Name": "testService",
}

@app.route('/', methods=['GET', 'POST'])
def main():
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7001)

