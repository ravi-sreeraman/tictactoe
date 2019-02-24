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
            set_values_to_empty(session)
            return render_template('index.html', game=session["board"], turn=session["turn"], message="X wins")
        else:
            session["turn"] = "O"
    else:
        if check_win("O"):
            set_values_to_empty(session)
            return render_template('index.html', game=session["board"], turn=session["turn"], message="X wins")
        else:
            session["turn"] = "X"
    return redirect(url_for("index"))


@app.route('/reset')
def reset():
    del session["board"]
    return redirect(url_for('index'))


def check_win(turn):
    row1 = session["board"][0][0] == turn and session["board"][0][1] == turn and session["board"][0][2] == turn
    row2 = session["board"][1][0] == turn and session["board"][1][1] == turn and session["board"][1][2] == turn
    row3 = session["board"][2][0] == turn and session["board"][2][1] == turn and session["board"][2][2] == turn
    col1 = session["board"][0][0] == turn and session["board"][1][0] == turn and session["board"][2][0] == turn
    col2 = session["board"][0][1] == turn and session["board"][1][1] == turn and session["board"][2][1] == turn
    col3 = session["board"][0][2] == turn and session["board"][1][2] == turn and session["board"][2][2] == turn
    d1 = session["board"][0][0] == turn and session["board"][1][1] == turn and session["board"][2][2] == turn
    d2 = session["board"][0][2] == turn and session["board"][1][1] == turn and session["board"][2][0] == turn
    return row1 or row2 or row3 or col1 or col2 or col3 or d1 or d2


def set_values_to_empty(session):
    for i in range(0, 3):
        for j in range(0, 3):
            if not session["board"][i][j]:
                session["board"][i][j] = ""
