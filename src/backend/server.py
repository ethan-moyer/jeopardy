from archiveparser import ArchiveParser
from flask import Flask
from flask import Response
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:8080")

global data
data = {}

global scores
scores = [0, 0, 0]

@socketio.on("store_first_set")
def store_first_set(game_id):
    parser = ArchiveParser(game_id)
    global data
    data = parser.get_first_set()
    emit("receive_data", data, broadcast=True)

@socketio.on("store_second_set")
def store_second_set(game_id):
    parser = ArchiveParser(game_id)
    global data
    data = parser.get_second_set()
    emit("receive_data", data)

@socketio.on("get_data")
def get_data():
    global data
    emit("receive_data", data)

@socketio.on("get_remaining_questions")
def get_remaining_questions():
    questions = []
    global data

    for row in range(5):
        for col in range(6):
            if data["questions"][row][col] is None:
                questions.append(False)
            else:
                questions.append(True)

    emit("receive_remaining_questions", questions)

@socketio.on("get_scores")
def get_scores():
    global scores
    emit("receive_scores", json.dumps(scores))

@socketio.on("change_score")
def change_score(player, points):
    global scores
    scores[int(player)] += int(points)
    emit("receive_scores", json.dumps(scores))

@socketio.on("show_question")
def show_question(r, c):
    global data
    data["questions"][r][c] = None
    emit("receive_data", data)

if __name__ == "__main__":
    socketio.run(app)