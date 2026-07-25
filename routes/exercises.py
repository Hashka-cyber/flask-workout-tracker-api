from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from config import db
from models import Exercise
from schemas import exercise_schema, exercises_schema


exercises_bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@exercises_bp.route("", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@exercises_bp.route("/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return jsonify(exercise_schema.dump(exercise)), 200


@exercises_bp.route("", methods=["POST"])
def create_exercise():
    json_data = request.get_json(silent=True)

    if not json_data:
        return jsonify({"error": "Request body must contain JSON data."}), 400

    try:
        data = exercise_schema.load(json_data)
        exercise = Exercise(**data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An exercise with this name already exists."}), 409


@exercises_bp.route("/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)

    db.session.delete(exercise)
    db.session.commit()

    return "", 204