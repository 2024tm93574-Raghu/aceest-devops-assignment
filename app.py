from flask import Flask, request, jsonify

app = Flask(__name__)

# Reuse idea from your desktop app: programs with calorie factors
PROGRAMS = {
    "Fat Loss FL 3 day": {"factor": 22, "description": "3-day full-body fat loss program"},
    "Fat Loss FL 5 day": {"factor": 24, "description": "5-day split, higher volume fat loss"},
    "Muscle Gain MG PPL": {"factor": 35, "description": "Push/Pull/Legs hypertrophy program"},
    "Beginner BG": {"factor": 26, "description": "3-day simple beginner full-body program"},
}


@app.route("/")
def home():
    return "ACEest Fitness Gym – DevOps Assignment Flask App"


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/programs", methods=["GET"])
def list_programs():
    """Return all available programs."""
    return jsonify(PROGRAMS), 200


@app.route("/recommend_calories", methods=["POST"])
def recommend_calories():
    """
    JSON body:
    {
      "weight": 75,
      "program": "Fat Loss FL 3 day"
    }
    """
    data = request.get_json() or {}
    weight = data.get("weight")
    program = data.get("program")

    if weight is None or program is None:
        return jsonify({"error": "weight and program are required"}), 400

    if program not in PROGRAMS:
        return jsonify({"error": "unknown program"}), 400

    factor = PROGRAMS[program]["factor"]
    calories = int(weight * factor)

    return jsonify(
        {
            "weight": weight,
            "program": program,
            "factor": factor,
            "recommended_calories": calories,
        }
    ), 200


if __name__ == "__main__":
    # For local development only
    app.run(host="0.0.0.0", port=5000)
