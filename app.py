from flask import Flask, render_template, request

app = Flask(__name__)

programs = {
    "Fat Loss": {
        "workout": """Mon: Squats + Core
Tue: HIIT Cardio
Wed: Bench Press
Thu: Deadlift
Fri: Zone 2 Cardio""",
        "diet": """Breakfast: Egg Whites + Oats
Lunch: Chicken + Brown Rice
Dinner: Fish + Millet""",
        "calorie_factor": 22
    },

    "Muscle Gain": {
        "workout": """Mon: Squat
Tue: Bench Press
Wed: Deadlift
Thu: Front Squat
Fri: Rows""",
        "diet": """Breakfast: Eggs + Oats
Lunch: Chicken Biryani
Dinner: Mutton Curry""",
        "calorie_factor": 35
    },

    "Beginner": {
        "workout": """Full Body Circuit
Pushups
Air Squats
Ring Rows""",
        "diet": """Balanced Diet
Idli / Dosa
Rice + Dal""",
        "calorie_factor": 26
    }
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
            return render_template("index.html", programs=programs.keys())

        weight = float(weight)
                
        p = programs[program]

        calories = int(weight * p["calorie_factor"])

        result = {
            "name": name,
            "age": age,
            "weight": weight,
            "program": program,
            "workout": p["workout"],
            "diet": p["diet"],
            "calories": calories
        }

    return render_template(
        "index.html",
        programs=programs.keys(),
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)