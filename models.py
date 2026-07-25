from datetime import date as date_type

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

ALLOWED_CATEGORIES = ("cardio", "strength", "flexibility", "balance", "other")


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date_type.today)
    duration_minutes = db.Column(db.Integer, nullable=False)

    # One workout has many workout_exercises (the join/association objects)
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )

    # Convenience many-to-many view straight to Exercise objects
    exercises = association_proxy("workout_exercises", "exercise")

    # ---------- Model (Python-level) validations ----------
    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Workout name cannot be empty.")
        return value.strip()

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        if value is None or int(value) <= 0:
            raise ValueError("Workout duration_minutes must be a positive integer.")
        return value

    def __repr__(self):
        return f"<Workout {self.id} {self.name}>"


class Exercise(db.Model):
    __tablename__ = "exercises"

    __table_args__ = (
        UniqueConstraint("name", name="uq_exercise_name"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )

    workouts = association_proxy("workout_exercises", "workout")

    # ---------- Model (Python-level) validations ----------
    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if value not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"Exercise category must be one of {ALLOWED_CATEGORIES}."
            )
        return value

    def __repr__(self):
        return f"<Exercise {self.id} {self.name}>"


class WorkoutExercise(db.Model):
    """Association object linking a Workout to an Exercise with set/rep/duration data."""

    __tablename__ = "workout_exercises"

    __table_args__ = (
        UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise"),
        CheckConstraint("sets > 0", name="ck_sets_positive"),
        CheckConstraint("reps > 0", name="ck_reps_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=True)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # ---------- Model (Python-level) validations ----------
    @validates("sets")
    def validate_sets(self, key, value):
        if value is None or int(value) <= 0:
            raise ValueError("sets must be a positive integer.")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is None or int(value) <= 0:
            raise ValueError("reps must be a positive integer.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and int(value) <= 0:
            raise ValueError("duration_seconds must be a positive integer if provided.")
        return value

    def __repr__(self):
        return f"<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>"