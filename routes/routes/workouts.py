from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from config import db
from models import Workout, Exercise, WorkoutExercise
from schemas import (
    workout_schema,
    workouts_schema,
    workout_exercise_schema,
)

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")


@workouts_bp.get("")
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@workouts_bp.get("/<int:workout_id>")
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return jsonify({"error": f"Workout {workout_id} not found."}), 404
    return jsonify(workout_schema.dump(workout)), 200


@workouts_bp.post("")
def create_workout():
    json_data = request.get_json(silent=True) or {}
    try:
        data = workout_schema.load(json_data, partial=("date",))
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    workout = Workout(
        name=data["name"],
        duration_minutes=data["duration_minutes"],
        date=data.get("date"),
    )
    try:
        db.session.add(workout)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 400

    return jsonify(workout_schema.dump(workout)), 201


@workouts_bp.delete("/<int:workout_id>")
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return jsonify({"error": f"Workout {workout_id} not found."}), 404
    db.session.delete(workout)
    db.session.commit()
    return jsonify({}), 204


@workouts_bp.post("/<int:workout_id>/exercises")
def add_exercise_to_workout(workout_id):
    """Add an existing exercise to a workout with sets/reps/duration."""
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return jsonify({"error": f"Workout {workout_id} not found."}), 404

    json_data = request.get_json(silent=True) or {}
    try:
        data = workout_exercise_schema.load(json_data, partial=("duration_seconds",))
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    exercise = db.session.get(Exercise, data["exercise_id"])
    if not exercise:
        return jsonify({"error": f"Exercise {data['exercise_id']} not found."}), 404

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        sets=data["sets"],
        reps=data["reps"],
        duration_seconds=data.get("duration_seconds"),
    )
    try:
        db.session.add(workout_exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 400

    return jsonify(workout_schema.dump(workout)), 201