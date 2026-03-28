from flask import Flask, render_template, request, redirect, jsonify
from models.db import init_db, get_connection
from datetime import date
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)
init_db()

programs = {
    "Fat Loss": 22,
    "Muscle Gain": 35,
    "Beginner": 26
}

# ---------- HOME ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form["name"]
            age = int(request.form["age"])
            weight = float(request.form["weight"])
            program = request.form["program"]

            calories = int(weight * programs[program])

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO clients(name, age, weight, program, calories)
                VALUES (?, ?, ?, ?, ?)
            """, (name, age, weight, program, calories))

            conn.commit()
            conn.close()

            return redirect("/dashboard")

        except Exception as e:
            return f"Error: {e}"

    return render_template("index.html", programs=programs)


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM clients")
    clients = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", clients=clients)


# ---------- DELETE CLIENT ----------
@app.route("/delete_client/<int:id>")
def delete_client(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM clients WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------- SAVE PROGRESS ----------
@app.route("/save_progress", methods=["POST"])
def save_progress():
    name = request.form["name"]
    adherence = request.form["adherence"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO progress (client_name, week, adherence) VALUES (?,?,?)",
        (name, str(date.today()), adherence)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------- LOG WORKOUT ----------
@app.route("/log_workout", methods=["POST"])
def log_workout():
    name = request.form["name"]
    workout = request.form["workout"]
    duration = request.form["duration"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO workouts(client_name,date,workout_type,duration) VALUES(?,?,?,?)",
        (name, str(date.today()), workout, duration)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------- LOG METRICS ----------
@app.route("/log_metrics", methods=["POST"])
def log_metrics():
    name = request.form["name"]
    weight = request.form["weight"]
    waist = request.form["waist"]
    bodyfat = request.form["bodyfat"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO metrics(client_name,date,weight,waist,bodyfat)
    VALUES(?,?,?,?,?)
    """, (name, str(date.today()), weight, waist, bodyfat))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------- HISTORY ----------
@app.route("/progress_history")
def progress_history():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM progress ORDER BY id DESC")
    data = cur.fetchall()

    conn.close()

    return render_template("progress.html", progress=data)


@app.route("/workout_history")
def workout_history():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM workouts ORDER BY id DESC")
    data = cur.fetchall()

    conn.close()

    return render_template("workouts.html", workouts=data)


@app.route("/metrics")
def metrics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM metrics ORDER BY id DESC")
    data = cur.fetchall()

    conn.close()

    return render_template("metrics.html", metrics=data)


# ---------- CHART ----------
@app.route("/progress_chart")
def progress_chart():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT adherence FROM progress")
    data = [x[0] for x in cur.fetchall()]

    conn.close()

    plt.figure()
    plt.plot(data)

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    graph = base64.b64encode(img.getvalue()).decode()

    return render_template("chart.html", graph=graph)


# ---------- API ----------
@app.route("/recommend_calories", methods=["POST"])
def recommend_calories():
    data = request.get_json()

    weight = float(data["weight"])
    program = data["program"]

    calories = int(weight * programs.get(program, 25))

    return jsonify({
        "recommended_calories": calories
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)