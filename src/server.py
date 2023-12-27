import json
import pickle
from threading import Thread
import time

# import pydantic
import flask
from flask import request
from flask_cors import CORS
from flask_socketio import SocketIO

app = flask.Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

### Global variables
clients = []
send_thread = None
current_state = None
###


### Rest APIs
@app.route("/data", methods=["GET"])
def data() -> flask.Response:
    data_file = "data.json"
    with open(data_file, "r") as f:
        data = json.load(f)
    return flask.jsonify(data)


### SocketIO


def send_data() -> None:
    while True:
        if current_state is None:
            continue
        socketio.emit("data", current_state)
        time.sleep(0.001)


@socketio.on("update")
def handle_update(data: str | dict) -> None:
    # print("New data received")
    global current_state
    if isinstance(data, str):
        data = json.loads(data)
    current_state = data


# @socketio.on("save")
# def handle_save(data: dict) -> None:
#     data_file = "data_saving.pkl"
#     with open(data_file, "wb") as f:
#         pickle.dump(data, f)
#     print("Data saved")


@socketio.on("connect")
def handle_connect() -> None:
    global send_thread

    session_id = request.sid
    if session_id not in clients:
        clients.append(session_id)
    print("Client connected", session_id)

    if send_thread is None:
        # just one for server
        # send_thread = Thread(target=send_data_DEBUG)
        send_thread = Thread(target=send_data)
        send_thread.start()


### Main
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=11000)

    args = parser.parse_args()
    socketio.run(app, host="0.0.0.0", port=args.port)
