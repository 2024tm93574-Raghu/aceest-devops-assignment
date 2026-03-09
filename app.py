from flask import Flask, render_template, request

app = Flask(__name__)

programs = {
    "Fat Loss": {
        "workout": "Squats, HIIT, Deadlifts",
        "diet": "Egg whites, chicken, fish"
    },
    "Muscle Gain": {
        "workout": "Squat, Bench, Deadlift",
        "diet": "Eggs, Biryani, Protein"
    },
    "Beginner": {
        "workout": "Pushups, Air squats",
        "diet": "Balanced diet"
    }
}

@app.route("/", methods=["GET","POST"])
def index():
    selected_program = None
    if request.method == "POST":
        program = request.form["program"]
        selected_program = programs.get(program)

    return render_template(
        "index.html",
        programs=programs.keys(),
        selected_program=selected_program
    )

if __name__ == "__main__":
    app.run(debug=True)