
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

WORKOUTS = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    return render_template("index.html", workouts=WORKOUTS)

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
        if request.is_json:
            return jsonify({"error": "Fields 'workout' and 'duration' are required"}), 400
        else:
            return redirect(url_for("home"))

    try:
        duration = int(duration)
    except ValueError:
        if request.is_json:
            return jsonify({"error": "Duration must be an integer"}), 400
        else:
            return redirect(url_for("home"))

    entry = {"workout": workout, "duration": duration}
    WORKOUTS.append(entry)

    if request.is_json:
        return jsonify(entry), 201
    else:
        return redirect(url_for("home"))

@app.get("/workouts")
def list_workouts():
    return jsonify({"count": len(WORKOUTS), "items": WORKOUTS})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
