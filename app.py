from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "12390123lkaslkjald_hi_Elie_Spencer_Brian_Sarah23123"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})

@app.post("/api/score-word")
def score_word():
    """Accepts JSON game ID and word, checks if word is valid and on board."""
    word_input = request.json
    gameId = word_input["gameId"]
    game = games[gameId]

    #return jsonify
    if not game.is_word_in_word_list(word_input["word"]):
        return jsonify({"result": "not-word"})
    elif not game.check_word_on_board(word_input["word"]):
        return jsonify({"result": "not-on-board"})
    else:
        game.play_and_score_word(word_input["word"])
        return jsonify({"result": "ok"})
