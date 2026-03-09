from flask import Flask, render_template, request, redirect
import sqlite3
from models.db import init_db

app = Flask(__name__)

init_db()

programs = {
    "Fat Loss": {"factor": 22},
    "Muscle Gain": {"factor": 35},
    "Beginner": {"factor": 26}
}

def get_db():
    return sqlite3.connect("database.db")

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


if __name__ == "__main__":
    app.run(debug=True)