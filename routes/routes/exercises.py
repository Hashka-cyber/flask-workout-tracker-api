from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from config import db
from models import Exercise
from schemas import exercise_schema, exercises_schema

exercises_bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@exercises_bp.get("")
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@exercises_bp.get("/<int:exercise_id>")
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return jsonify({"error": f"Exercise {exercise_id} not found."}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@exercises_bp.post("")
def create_exercise():
    json_data = request.get_json(silent=True) or {}
    try:
        data = exercise_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    exercise = Exercise(
        name=data["name"],
        category=data["category"],
        equipment_needed=data.get("equipment_needed", False),
    )
    try:
        db.session.add(exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"error": "Exercise name must be unique."}), 400

    return jsonify(exercise_schema.dump(exercise)), 201


@exercises_bp.delete("/<int:exercise_id>")
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return jsonify({"error": f"Exercise {exercise_id} not found."}), 404
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({}), 204