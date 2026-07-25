from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from config import db
from models import Exercise, Workout, WorkoutExercise
from schemas import (
    workout_exercise_schema,
    workout_schema,
    workouts_schema,
)


workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")


@workouts_bp.route("", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.date.desc(), Workout.id.desc()).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@workouts_bp.route("/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return jsonify(workout_schema.dump(workout)), 200


@workouts_bp.route("", methods=["POST"])
def create_workout():
    json_data = request.get_json(silent=True)

    if not json_data:
        return jsonify({"error": "Request body must contain JSON data."}), 400

    try:
        data = workout_schema.load(json_data)
        workout = Workout(**data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


@workouts_bp.route("/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    db.session.delete(workout)
    db.session.commit()

    return "", 204


@workouts_bp.route("/<int:workout_id>/exercises", methods=["POST"])
def add_exercise_to_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    json_data = request.get_json(silent=True)

    if not json_data:
        return jsonify({"error": "Request body must contain JSON data."}), 400

    try:
        data = workout_exercise_schema.load(json_data)

        exercise = Exercise.query.get(data["exercise_id"])

        if exercise is None:
            return jsonify({"error": "Exercise not found."}), 404

        workout_exercise = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            sets=data["sets"],
            reps=data["reps"],
            duration_seconds=data.get("duration_seconds"),
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify(
            {"error": "This exercise has already been added to this workout."}
        ), 409