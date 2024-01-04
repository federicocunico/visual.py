import json
import pickle
from threading import Thread
import time

# import pydantic
import flask
from flask import request
from flask_cors import CORS
from flask_socketio import SocketIO

from .cfg import STATIC_PATH

app = flask.Flask(__name__, static_folder=STATIC_PATH, static_url_path="")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
server_main_thread = None

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


@app.route("/", methods=["GET"])
def index() -> flask.Response:
    # send html file in static folder
    return app.send_static_file("index.html")


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
def server_socket_main_thread(port: int):
    global server_main_thread

    if server_main_thread is None:
        # First time running the app? Then serve it!
        def serve():
            socketio.run(app, host="0.0.0.0", port=port)

        server_main_thread = Thread(target=serve)
        server_main_thread.start()
    return server_main_thread


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=40000)

    args = parser.parse_args()
    _t = server_socket_main_thread(args.port)
    _t.join()
