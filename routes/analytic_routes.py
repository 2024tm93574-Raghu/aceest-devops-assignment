from flask import render_template, redirect, session, Blueprint
from models.db import init_db, get_connection

analytic_bp = Blueprint("analytic", __name__)

init_db()


# ---------- PROGRESS HISTORY ----------
@analytic_bp.route("/progress_history")
def progress_history():
    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM progress ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()

    return render_template("progress.html", progress=data)


# ---------- WORKOUT HISTORY ----------
@analytic_bp.route("/workout_history")
def workout_history():
    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM workouts ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()

    return render_template("workouts.html", workouts=data)


# ---------- BODY METRICS ----------
@analytic_bp.route("/metrics")
def metrics():
    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM metrics ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()

    return render_template("metrics.html", metrics=data)