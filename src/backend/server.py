from archiveparser import ArchiveParser
from flask import Flask
from flask import Response
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

data = {}
scores = [0, 0, 0]

@app.route("/store_first_set/<game_id>", methods=["GET"])
def store_first_set(game_id):
    parser = ArchiveParser(game_id)
    data = parser.get_first_set()
    return data

@app.route("/store_second_set/<game_id>", methods=["GET"])
def store_second_set(game_id):
    parser = ArchiveParser(game_id)
    data = parser.get_second_set()
    return data

@app.route("/scores", methods=["GET"])
def get_scores():
    return Response(json.dumps(scores), mimetype="application/json")

@app.route("/change_score/<player>/<points>", methods=["GET"])
def change_score(player, points):
    scores[int(player)] += int(points)
    return Response(json.dumps(scores), mimetype="application/json")

if __name__ == "__main__":
    socketio.run(app)