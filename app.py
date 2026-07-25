from flask import Flask

from config import db
from routes import exercises_bp, workouts_bp


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workouts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(workouts_bp)
app.register_blueprint(exercises_bp)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {
        "message": "Workout Tracker API is running",
        "endpoints": {
            "workouts": "/workouts",
            "exercises": "/exercises",
        },
    }, 200


if __name__ == "__main__":
    app.run(debug=True)