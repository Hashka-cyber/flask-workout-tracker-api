from flask import Flask
from config import db
from models import Workout, Exercise, WorkoutExercise

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workouts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {"message": "Workout Tracker API is running"}


if __name__ == "__main__":
    app.run(debug=True)