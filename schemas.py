from marshmallow import fields, validate, validates, ValidationError

from config import BaseSchema
from models import ALLOWED_CATEGORIES


class ExerciseSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100, error="name must be 1-100 characters."),
    )
    category = fields.String(
        required=True,
        validate=validate.OneOf(ALLOWED_CATEGORIES),
    )
    equipment_needed = fields.Boolean(load_default=False)

    @validates("name")
    def validate_name_not_blank(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("name cannot be blank or whitespace.")


class WorkoutExerciseSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(required=True)
    sets = fields.Integer(required=True, validate=validate.Range(min=1, max=50))
    reps = fields.Integer(required=True, validate=validate.Range(min=1, max=1000))
    duration_seconds = fields.Integer(
        required=False, allow_none=True, validate=validate.Range(min=1)
    )
    # nested read-only view of the exercise so responses are self-descriptive
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100, error="name must be 1-100 characters."),
    )
    date = fields.Date(required=False)
    duration_minutes = fields.Integer(
        required=True, validate=validate.Range(min=1, max=600)
    )
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema), dump_only=True
    )

    @validates("name")
    def validate_name_not_blank(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("name cannot be blank or whitespace.")


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()