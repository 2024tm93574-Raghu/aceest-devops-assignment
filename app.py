from flask import Flask, render_template, request, redirect
import sqlite3
from models.db import init_db
import jsonify

app = Flask(__name__)

init_db()

programs = {
    "Fat Loss": {"factor": 22},
    "Muscle Gain": {"factor": 35},
    "Beginner": {"factor": 26}
}

def get_db():
    return sqlite3.connect("database.db")

@app.route("/progress", methods=["POST"])
def save_progress():

    name = request.form["name"]
    adherence = request.form["adherence"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO progress(client_name,week,adherence)
    VALUES(?,?,?)
    """,(name,"week1",adherence))

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

if __name__ == "__main__":
    app.run(debug=True)