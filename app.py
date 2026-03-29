from flask import Flask, render_template, request, redirect, jsonify, session
from models.db import init_db, get_connection
from datetime import date
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io, base64, random
from routes.client_routes import client_bp
from routes.analytic_routes import analytic_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

init_db()

app.register_blueprint(client_bp)
app.register_blueprint(analytic_bp)

# ---------- PROGRAM DATA ----------
programs = {
    "Fat Loss": 22,
    "Muscle Gain": 35,
    "Beginner": 26
}

workout_plans = {
    "Fat Loss": "Mon: Back Squat 5x5\nTue: EMOM Cardio 20min\nWed: Bench Press\nThu: Deadlifts\nFri: Active Recovery",
    "Muscle Gain": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat\nFri: Rows 4x10",
    "Beginner": "Full Body Circuit:\nAir Squats, Ring Rows, Push-ups\nFocus: Technique & Form"
}

diet_plans = {
    "Fat Loss": "B: Egg Whites + Oats\nL: Grilled Chicken + Brown Rice\nD: Fish Curry + Millet Roti\nTarget: ~2000 kcal",
    "Muscle Gain": "B: 4 Eggs + Peanut Butter Oats\nL: Chicken Biryani\nD: Mutton Curry + Rice\nTarget: ~3200 kcal",
    "Beginner": "Balanced Meals: Idli/Dosa/Rice + Dal\nProtein Target: 120g/day"
}

# AI exercise pool (from professor's v3.1.2)
exercise_pool = {
    "Fat Loss": ["Running", "Cycling", "Rowing", "Burpees", "Jump Rope", "Kettlebell Swings", "Box Jumps", "Battle Ropes"],
    "Muscle Gain": ["Squat", "Deadlift", "Bench Press", "Overhead Press", "Pull-Up", "Barbell Row", "Leg Press", "Incline Dumbbell Press"],
    "Beginner": ["Push-Up", "Pull-Up", "Lunge", "Plank", "Dumbbell Row", "Air Squat", "Dumbbell Press", "Glute Bridge"]
}

experience_config = {
    "beginner":     {"sets": (2, 3), "reps": (8, 12),  "days": ["Monday", "Wednesday", "Friday"]},
    "intermediate": {"sets": (3, 4), "reps": (8, 15),  "days": ["Monday", "Tuesday", "Thursday", "Friday"]},
    "advanced":     {"sets": (4, 5), "reps": (6, 15),  "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
}


# ---------- HOME — ADD CLIENT ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        weight = request.form["weight"]
        program = request.form["program"]

        factor = programs.get(program, 25)
        calories = int(float(weight) * factor)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO clients (name, age, weight, program, calories) VALUES (?,?,?,?,?)",
            (name, age, weight, program, calories)
        )
        conn.commit()
        conn.close()

        result = {
            "name": name,
            "age": age,
            "weight": weight,
            "program": program,
            "calories": calories,
            "workout": workout_plans.get(program, ""),
            "diet": diet_plans.get(program, "")
        }
        return render_template("index.html", programs=list(programs.keys()), result=result)

    return render_template("index.html", programs=list(programs.keys()))


# ---------- VIEW CLIENT PLAN (trainer can revisit anytime) ----------
@app.route("/client_plan/<client_name>")
def client_plan(client_name):
    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE name=?", (client_name,))
    c = cur.fetchone()
    conn.close()

    if not c:
        return redirect("/dashboard")

    # c = (id, name, age, weight, program, calories)
    program = c[4]
    result = {
        "name": c[1],
        "age": c[2],
        "weight": c[3],
        "program": program,
        "calories": c[5],
        "workout": workout_plans.get(program, "No plan available"),
        "diet": diet_plans.get(program, "No plan available")
    }
    return render_template("client_plan.html", result=result)


# ---------- AI PROGRAM GENERATOR ----------
@app.route("/ai_program/<client_name>", methods=["GET", "POST"])
def ai_program(client_name):
    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE name=?", (client_name,))
    c = cur.fetchone()
    conn.close()

    if not c:
        return redirect("/dashboard")

    program = c[4]  # e.g. "Fat Loss"
    generated = None

    if request.method == "POST":
        experience = request.form.get("experience", "beginner").lower()
        config = experience_config.get(experience, experience_config["beginner"])
        pool = exercise_pool.get(program, exercise_pool["Beginner"])

        generated = []
        for day in config["days"]:
            exercises = random.sample(pool, k=min(4, len(pool)))
            for ex in exercises:
                sets = random.randint(*config["sets"])
                reps = random.randint(*config["reps"])
                generated.append({
                    "day": day,
                    "exercise": ex,
                    "sets": sets,
                    "reps": reps
                })

    return render_template("ai_program.html",
                           client_name=client_name,
                           program=program,
                           generated=generated)


# ---------- SAVE PROGRESS ----------
@app.route("/save_progress", methods=["POST"])
def save_progress():
    if "user" not in session:
        return redirect("/login")
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
    if "user" not in session:
        return redirect("/login")
    name = request.form["name"]
    workout = request.form["workout"]
    duration = request.form["duration"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO workouts(client_name, date, workout_type, duration) VALUES(?,?,?,?)",
        (name, str(date.today()), workout, duration)
    )
    conn.commit()
    conn.close()
    return redirect("/dashboard")


# ---------- LOG METRICS ----------
@app.route("/log_metrics", methods=["POST"])
def log_metrics():
    if "user" not in session:
        return redirect("/login")
    name = request.form["name"]
    weight = request.form["weight"]
    waist = request.form["waist"]
    bodyfat = request.form["bodyfat"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO metrics(client_name, date, weight, waist, bodyfat) VALUES(?,?,?,?,?)",
        (name, str(date.today()), weight, waist, bodyfat)
    )
    conn.commit()
    conn.close()
    return redirect("/dashboard")


# ---------- PROGRESS CHART — PER CLIENT ----------
@app.route("/progress_chart/<client_name>")
def progress_chart(client_name):
    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT week, adherence FROM progress WHERE client_name=? ORDER BY id",
        (client_name,)
    )
    rows = cur.fetchall()
    conn.close()

    plt.figure(figsize=(8, 4))
    if rows:
        weeks = [r[0] for r in rows]
        adherence = [r[1] for r in rows]
        plt.plot(weeks, adherence, marker="o", color="#d4af37", linewidth=2)
        plt.xticks(rotation=45, ha="right")
    else:
        plt.text(0.5, 0.5, "No progress data yet for this client",
                 ha="center", va="center", transform=plt.gca().transAxes)

    plt.title(f"Adherence Progress — {client_name}")
    plt.ylabel("Adherence %")
    plt.xlabel("Date")
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()

    graph = base64.b64encode(img.getvalue()).decode()
    return render_template("chart.html", graph=graph, client_name=client_name)


# ---------- CALORIES API ----------
@app.route("/recommend_calories", methods=["POST"])
def recommend_calories():
    data = request.get_json()
    weight = float(data["weight"])
    program = data["program"]
    calories = int(weight * programs.get(program, 25))
    return jsonify({"recommended_calories": calories})


# ---------- HEALTH ----------
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html",
                                   error="Invalid credentials. Default: admin / admin")

    return render_template("login.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
