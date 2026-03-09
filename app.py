from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from models.db import init_db
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

init_db()

programs = {
    "Fat Loss": {"factor": 22},
    "Muscle Gain": {"factor": 35},
    "Beginner": {"factor": 26}
}

def get_db():
    return sqlite3.connect("database.db")

@app.route("/save_progress", methods=["POST"])
def save_progress():

    name = request.form["name"]
    adherence = request.form["adherence"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO progress (client_name, week, adherence) VALUES (?,?,?)",
        (name, "Week 1", adherence)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/", methods=["GET","POST"])
def index():

    result = None

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        weight = float(request.form["weight"])
        program = request.form["program"]

        calories = int(weight * programs[program]["factor"])

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO clients(name,age,weight,program,calories)
        VALUES(?,?,?,?,?)
        """,(name,age,weight,program,calories))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("index.html", programs=programs)


@app.route("/dashboard")
def dashboard():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM clients")
    clients = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", clients=clients)


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/progress_history")
def progress_history():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM progress ORDER BY id DESC")
    progress = cur.fetchall()

    conn.close()

    return render_template("progress.html", progress=progress)

@app.route("/recommend_calories", methods=["POST"])
def recommend_calories():

    data = request.get_json()

    if not data or "weight" not in data or "program" not in data:
        return jsonify({"error": "missing fields"}), 400

    weight = float(data["weight"])
    program = data["program"]

    programs = {
        "Fat Loss FL 3 day": 22,
        "Muscle Gain MG": 35,
        "Beginner BG": 26
    }

    factor = programs.get(program)

    if not factor:
        return jsonify({"error": "invalid program"}), 400

    calories = int(weight * factor)

    return jsonify({
        "weight": weight,
        "program": program,
        "recommended_calories": calories
    }), 200

@app.route("/progress_chart")
def progress_chart():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT adherence FROM progress")
    data = cur.fetchall()

    conn.close()

    values = [d[0] for d in data]

    plt.figure()
    plt.plot(values)

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    graph = base64.b64encode(img.getvalue()).decode()

    return render_template("chart.html", graph=graph)

@app.route("/log_workout", methods=["POST"])
def log_workout():

    name = request.form["name"]
    workout = request.form["workout"]
    duration = request.form["duration"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO workouts(client_name,date,workout_type,duration) VALUES(?,?,?,?)",
        (name,"today",workout,duration)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)