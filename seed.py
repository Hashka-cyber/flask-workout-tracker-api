from datetime import date

from app import app
from config import db
from models import Workout, Exercise, WorkoutExercise


with app.app_context():
    print("Deleting old data...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Creating exercises...")

    squat = Exercise(
        name="Squat",
        category="strength",
        equipment_needed=False,
    )

    push_up = Exercise(
        name="Push Up",
        category="strength",
        equipment_needed=False,
    )

    running = Exercise(
        name="Running",
        category="cardio",
        equipment_needed=False,
    )

    yoga = Exercise(
        name="Yoga Stretch",
        category="flexibility",
        equipment_needed=False,
    )

    db.session.add_all([squat, push_up, running, yoga])
    db.session.commit()

    print("Creating workouts...")

    morning_workout = Workout(
        name="Morning Strength Workout",
        date=date.today(),
        duration_minutes=45,
    )

    cardio_workout = Workout(
        name="Cardio Session",
        date=date.today(),
        duration_minutes=30,
    )

    flexibility_workout = Workout(
        name="Evening Stretch",
        date=date.today(),
        duration_minutes=20,
    )

    db.session.add_all(
        [
            morning_workout,
            cardio_workout,
            flexibility_workout,
        ]
    )
    db.session.commit()

    print("Linking exercises to workouts...")

    workout_exercise_1 = WorkoutExercise(
        workout_id=morning_workout.id,
        exercise_id=squat.id,
        sets=4,
        reps=12,
    )

    workout_exercise_2 = WorkoutExercise(
        workout_id=morning_workout.id,
        exercise_id=push_up.id,
        sets=3,
        reps=15,
    )

    workout_exercise_3 = WorkoutExercise(
        workout_id=cardio_workout.id,
        exercise_id=running.id,
        sets=1,
        reps=1,
        duration_seconds=1800,
    )

    workout_exercise_4 = WorkoutExercise(
        workout_id=flexibility_workout.id,
        exercise_id=yoga.id,
        sets=3,
        reps=10,
        duration_seconds=600,
    )

    db.session.add_all(
        [
            workout_exercise_1,
            workout_exercise_2,
            workout_exercise_3,
            workout_exercise_4,
        ]
    )

    db.session.commit()

    print("Database seeded successfully.")