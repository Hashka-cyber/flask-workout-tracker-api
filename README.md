# Workout Tracker API

A Flask + SQLAlchemy + Marshmallow backend for a workout tracking application used by
personal trainers. Trainers can create workouts and reusable exercises, then attach
exercises to a workout with specific sets, reps, and/or duration.

## Description

- **Workout**: a training session (name, date, duration_minutes).
- **Exercise**: a reusable movement (name, category, equipment_needed) that can belong
  to many workouts.
- **WorkoutExercise**: the join table between Workout and Exercise, storing the
  sets/reps/duration_seconds specific to that exercise *in that workout*.

## Installation

\`\`\`bash
pipenv install
pipenv shell

export FLASK_APP=app.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade

python seed.py
\`\`\`

## Running the app

\`\`\`bash
flask run -p 5555
\`\`\`

The API will be available at `http://127.0.0.1:5555`.

## Endpoints

| Method | Route                      | Description                                             |
|--------|-----------------------------|-----------------------------------------------------------|
| GET    | `/`                          | API index / list of endpoints                             |
| GET    | `/workouts`                  | List all workouts (with their exercises)                   |
| GET    | `/workouts/<id>`             | Get one workout by id                                       |
| POST   | `/workouts`                  | Create a workout — body: `name`, `duration_minutes`, `date?` |
| DELETE | `/workouts/<id>`             | Delete a workout (cascades its workout_exercise records)     |
| POST   | `/workouts/<id>/exercises`   | Add an exercise to a workout — body: `exercise_id`, `sets`, `reps`, `duration_seconds?` |
| GET    | `/exercises`                 | List all exercises                                           |
| GET    | `/exercises/<id>`            | Get one exercise by id                                        |
| POST   | `/exercises`                 | Create an exercise — body: `name`, `category`, `equipment_needed?` |
| DELETE | `/exercises/<id>`            | Delete an exercise (cascades its workout_exercise records)      |

### Validations

**Table constraints**
- `exercises.name` — `UNIQUE`
- `workout_exercises` — `UNIQUE(workout_id, exercise_id)`
- `workout_exercises.sets > 0` / `.reps > 0` — `CHECK` constraints
- `workouts.duration_minutes > 0` — `CHECK` constraint

**Model validations** (`@validates`)
- `Workout.name` / `Exercise.name` cannot be blank
- `Workout.duration_minutes` must be a positive integer
- `Exercise.category` must be one of `cardio, strength, flexibility, balance, other`
- `WorkoutExercise.sets` / `.reps` must be positive integers
- `WorkoutExercise.duration_seconds` must be positive if provided

**Schema validations** (Marshmallow)
- `name` length between 1 and 100 characters
- `category` restricted via `validate.OneOf(...)`
- `sets`, `reps`, `duration_minutes`, `duration_seconds` restricted via `validate.Range(...)`