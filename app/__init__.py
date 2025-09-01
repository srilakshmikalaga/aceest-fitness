from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

WORKOUTS = []


@app.get("/")
def home():
    total = sum(w["duration"] for w in WORKOUTS)
    avg = (total / len(WORKOUTS)) if WORKOUTS else 0
    longest = max(WORKOUTS, key=lambda x: x["duration"], default=None)
    shortest = min(WORKOUTS, key=lambda x: x["duration"], default=None)

    stats = {
        "count": len(WORKOUTS),
        "total_duration": total,
        "average_duration": avg,
        "longest": longest,
        "shortest": shortest,
    }
    return render_template("index.html", workouts=WORKOUTS, stats=stats)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/workouts")
def list_workouts():
    return jsonify({"count": len(WORKOUTS), "items": WORKOUTS})


@app.get("/workouts/<int:workout_id>")
def get_workout(workout_id):
    if workout_id < 0 or workout_id >= len(WORKOUTS):
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(WORKOUTS[workout_id])


@app.post("/workouts")
def add_workout():
    if request.is_json:
        data = request.get_json(silent=True) or {}
        workout = data.get("workout")
        duration = data.get("duration")
    else:
        workout = request.form.get("workout")
        duration = request.form.get("duration")

    if not workout or duration is None:
        return jsonify({"error": "Fields 'workout' and 'duration' are required"}), 400

    try:
        duration = int(duration)
    except ValueError:
        return jsonify({"error": "Duration must be an integer"}), 400

    new_workout = {"workout": workout, "duration": duration}
    WORKOUTS.append(new_workout)

    if request.is_json:
        return jsonify(new_workout), 201
    return redirect(url_for("home"))


@app.route("/workouts/<int:workout_id>", methods=["PUT", "POST"])
def update_workout(workout_id):
    if workout_id < 0 or workout_id >= len(WORKOUTS):
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json(silent=True) or request.form
    workout = data.get("workout")
    duration = data.get("duration")

    if not workout or duration is None:
        return jsonify({"error": "Fields 'workout' and 'duration' are required"}), 400

    try:
        duration = int(duration)
    except ValueError:
        return jsonify({"error": "Duration must be an integer"}), 400

    WORKOUTS[workout_id] = {"workout": workout, "duration": duration}
    return redirect(url_for("home")) if not request.is_json else jsonify(WORKOUTS[workout_id])


@app.get("/stats")
def stats():
    if not WORKOUTS:
        return jsonify({"count": 0, "total_duration": 0, "average_duration": 0})
    total = sum(w["duration"] for w in WORKOUTS)
    avg = total / len(WORKOUTS)
    return jsonify({"count": len(WORKOUTS), "total_duration": total, "average_duration": avg})


@app.get("/longest")
def longest_workout():
    if not WORKOUTS:
        return jsonify({"error": "No workouts available"}), 404
    longest = max(WORKOUTS, key=lambda x: x["duration"])
    return jsonify(longest)


@app.get("/shortest")
def shortest_workout():
    if not WORKOUTS:
        return jsonify({"error": "No workouts available"}), 404
    shortest = min(WORKOUTS, key=lambda x: x["duration"])
    return jsonify(shortest)


@app.get("/search")
def search_workouts():
    query = request.args.get("name", "").lower()
    results = [w for w in WORKOUTS if query in w["workout"].lower()]
    return jsonify({"count": len(results), "items": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
