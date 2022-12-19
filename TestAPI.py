from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods =['POST'])
def hello_world():
    if not request.is_json:
        return {"err" : "NotgoodFormat"} , 401 
    req_json =  request.get_json()
    res_json = {
        "res_chat": "hello " + req_json["name"],
        "question": "what do you mean " + req_json["chat"]
    }
    return res_json



if __name__ == '__main__':
    app.run(debug=True)