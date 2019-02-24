from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

win = False
@app.route('/')
def index():
    if "board" not in session:
        session["board"] = [[None, None, None], [
            None, None, None], [None, None, None]]
        session["turn"] = "X"

    return render_template('index.html', game=session["board"], turn=session["turn"])


@app.route('/play/<int:row>/<int:col>')
def play(row, col):
    session["board"][row][col] = session["turn"]
    if session["turn"] == "X":
        if check_win("X"):
            return "X wins"
        session["turn"] = "O"
    else:
        session["turn"] = "X"
        if check_win("Y"):
            return "Y wins"
    return redirect(url_for("index"))


@app.route('/reset')
def reset():
    del session["board"]
    return redirect(url_for('index'))


def check_win(turn):
    rows = session["board"][0][0] == turn and session["board"][0][1] == turn and session["board"][0][2] == turn
    return rows
