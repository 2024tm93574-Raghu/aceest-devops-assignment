from flask import Flask, render_template, request
import sqlite3
from models.db import init_db

app = Flask(__name__)

init_db()

programs = {
    "Fat Loss": {"factor":22},
    "Muscle Gain": {"factor":35},
    "Beginner": {"factor":26}
}

@app.route("/", methods=["GET","POST"])
def index():

    result = None

    if request.method == "POST":

        name = request.form.get("name")
        age = request.form.get("age")
        weight = request.form.get("weight")
        program = request.form.get("program")

        if not weight:
            return render_template("index.html", programs=programs)

        weight = float(weight)
        calories = int(weight * programs[program]["factor"])

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO clients(name,age,weight,program,calories)
        VALUES(?,?,?,?,?)
        """,(name,age,weight,program,calories))

        conn.commit()
        conn.close()

        result = {
            "name":name,
            "age":age,
            "weight":weight,
            "program":program,
            "calories":calories
        }

    return render_template("index.html",
                           programs=programs,
                           result=result)

if __name__ == "__main__":
    app.run(debug=True)