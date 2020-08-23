from archiveparser import ArchiveParser
from flask import Flask
from flask import Response
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

global data
data = {}

global scores
scores = [0, 0, 0]

def player_data():
    global data
    questions = []

    for row in range(5):
        for col in range(6):
            if data["questions"][row][col] is None:
                questions.append(False)
            else:
                questions.append(True)

    return {"categories": data["categories"], "questions": questions}

@socketio.on("load_data")
def load_data(game_id, round):
    global data
    global scores
    parser = ArchiveParser(game_id)
    data = parser.get_first_set() if round == 1 else parser.get_second_set()

    emit("receive_data", player_data(), broadcast=True)
    emit("receive_data_host", (data, scores), broadcast=True)

@socketio.on("get_data")
def get_data():
    emit("receive_data", player_data(), broadcast=True)

@socketio.on("get_data_host")
def get_data_host():
    global data
    global scores
    emit("receive_data_host", (data, scores), broadcast=True)

@socketio.on("remove_question")
def remove_question(row, col):
    global data
    data["questions"][row][col] = None
    emit("close_question", broadcast=True)
    emit("receive_data", player_data(), broadcast=True)
    emit("receive_data_host", (data, scores), broadcast=True)

@socketio.on("open_question")
def open_question(row, col):
    global data
    emit("open_question", data["questions"][row][col], broadcast=True)

@socketio.on("change_score")
def change_score(player, points):
    global scores
    scores[int(player)] += int(points)
    emit("receive_data_host", (data, scores), broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")