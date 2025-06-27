# app.py
#!/usr/bin/env python3
"""
Flask server for the multi-game hub, with
“Fifty Most Common English Words” and
“Two Hundred Most Common English Words” Aristocrat cipher games.
"""

from flask import Flask, render_template, jsonify, request
from games.aristocrat import AristocratGame

app = Flask(__name__, static_folder="static", template_folder="templates")

# Fifty Most Common English Words instance
game_fifty = AristocratGame(
    words_file="data/MostCommonEnglishWords.txt",
    quotes_file="data/English_Quotes.xlsx"
)

# Two Hundred Most Common English Words instance
game_two_hundred = AristocratGame(
    words_file="data/EnglishWords.txt",
    quotes_file="data/English_Quotes.xlsx"
)


@app.route("/")
def home():
    """Home page with links to each game."""
    return render_template("home.html")


@app.route("/fifty")
def fifty_game():
    """Page for Fifty Most Common English Words cipher game."""
    return render_template(
        "aristocrat.html",
        api_prefix="/api/fifty",
        game_title="Fifty Most Common English Words"
    )


@app.route("/twohundred")
def two_hundred_game():
    """Page for Two Hundred Most Common English Words cipher game."""
    return render_template(
        "aristocrat.html",
        api_prefix="/api/twohundred",
        game_title="Two Hundred Most Common English Words"
    )


@app.route("/api/fifty/new-round", methods=["GET"])
def new_round_fifty():
    game_fifty.generate_cipher()
    return jsonify({
        "tokens": game_fifty.get_cipher_tokens(),
        "freqs":  game_fifty.get_token_frequencies()
    })


@app.route("/api/fifty/check", methods=["POST"])
def check_fifty():
    data = request.get_json() or {}
    correct = game_fifty.check_guess(data.get("guess", ""))
    answer  = game_fifty.plaintext
    return jsonify({"correct": correct, "answer": answer})


@app.route("/api/twohundred/new-round", methods=["GET"])
def new_round_twohundred():
    game_two_hundred.generate_cipher()
    return jsonify({
        "tokens": game_two_hundred.get_cipher_tokens(),
        "freqs":  game_two_hundred.get_token_frequencies()
    })


@app.route("/api/twohundred/check", methods=["POST"])
def check_twohundred():
    data = request.get_json() or {}
    correct = game_two_hundred.check_guess(data.get("guess", ""))
    answer  = game_two_hundred.plaintext
    return jsonify({"correct": correct, "answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
