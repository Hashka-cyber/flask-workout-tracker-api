# Workout Tracker API

A backend REST API for a workout tracking application built with Flask, SQLAlchemy, and Marshmallow.

The application allows personal trainers to create workouts, create reusable exercises, connect exercises to workouts, and store sets, reps, and duration information.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Marshmallow
- SQLite
- Pipenv
- Git and GitHub

## Project Structure

```text
flask-workout-tracker-api/
│
├── routes/
│   ├── __init__.py
│   ├── exercises.py
│   └── workouts.py
│
├── app.py
├── config.py
├── models.py
├── schemas.py
├── seed.py
├── Pipfile
├── Pipfile.lock
├── README.md
└── .gitignore
```

## Models

### Workout

A workout represents a training session.

Fields:

- `id`
- `name`
- `date`
- `duration_minutes`

A workout can contain multiple exercises through the `WorkoutExercise` model.

### Exercise

An exercise is a reusable movement that can be added to different workouts.

Fields:

- `id`
- `name`
- `category`
- `equipment_needed`

Allowed exercise categories:

- `cardio`
- `strength`
- `flexibility`
- `balance`
- `other`

### WorkoutExercise

`WorkoutExercise` is the association model that connects a workout to an exercise.

Fields:

- `id`
- `workout_id`
- `exercise_id`
- `sets`
- `reps`
- `duration_seconds`

This model stores information specific to an exercise inside a workout.

## Installation

Clone the repository:

```bash
git clone https://github.com/Hashka-cyber/flask-workout-tracker-api.git
```

Enter the project folder:

```bash
cd flask-workout-tracker-api
```

Install the project dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

## Database Setup

The application creates the SQLite database tables automatically when `app.py` is imported or started.

Create starter data by running:

```bash
python seed.py
```

Expected output:

```text
Deleting old data...
Creating exercises...
Creating workouts...
Linking exercises to workouts...
Database seeded successfully.
```

## Running the Application

Start the Flask server:

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check that the API is running |
| GET | `/workouts` | View all workouts |
| GET | `/workouts/<id>` | View one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| POST | `/workouts/<id>/exercises` | Add an exercise to a workout |
| GET | `/exercises` | View all exercises |
| GET | `/exercises/<id>` | View one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

## Request Examples

### Create a Workout

Request:

```http
POST /workouts
```

JSON body:

```json
{
  "name": "Upper Body Workout",
  "date": "2026-07-26",
  "duration_minutes": 45
}
```

Example successful response:

```json
{
  "id": 4,
  "name": "Upper Body Workout",
  "date": "2026-07-26",
  "duration_minutes": 45,
  "workout_exercises": []
}
```

### Create an Exercise

Request:

```http
POST /exercises
```

JSON body:

```json
{
  "name": "Bench Press",
  "category": "strength",
  "equipment_needed": true
}
```

Example successful response:

```json
{
  "id": 5,
  "name": "Bench Press",
  "category": "strength",
  "equipment_needed": true
}
```

### Add an Exercise to a Workout

Request:

```http
POST /workouts/1/exercises
```

JSON body:

```json
{
  "exercise_id": 5,
  "sets": 4,
  "reps": 10,
  "duration_seconds": null
}
```

### Delete a Workout

Request:

```http
DELETE /workouts/1
```

Successful response status:

```text
204 No Content
```

### Delete an Exercise

Request:

```http
DELETE /exercises/5
```

Successful response status:

```text
204 No Content
```

## Validations

The application includes validation at the database, model, and schema levels.

### Table Constraints

- Workout duration must be greater than zero.
- Exercise names must be unique.
- The same exercise cannot be added to the same workout more than once.
- Sets must be greater than zero.
- Reps must be greater than zero.
- Foreign keys connect workouts and exercises correctly.

### Model Validations

- Workout names cannot be empty.
- Exercise names cannot be empty.
- Workout duration must be a positive integer.
- Exercise category must be one of the allowed categories.
- Sets must be a positive integer.
- Reps must be a positive integer.
- Duration in seconds must be positive when provided.

### Schema Validations

- Workout and exercise names must contain between 1 and 100 characters.
- Categories must match one of the allowed values.
- Workout duration must be between 1 and 600 minutes.
- Sets must be between 1 and 50.
- Reps must be between 1 and 1000.
- Duration in seconds must be greater than zero when provided.

## Error Handling

The API returns suitable HTTP status codes:

- `200 OK` for successful GET requests
- `201 Created` when a record is created
- `204 No Content` when a record is deleted
- `400 Bad Request` for invalid request data
- `404 Not Found` when a workout or exercise does not exist
- `409 Conflict` when duplicate data violates a unique constraint

## Testing

The API can be tested using:

- A browser for GET requests
- Postman
- Thunder Client
- curl

Example:

```bash
curl http://127.0.0.1:5000/workouts
```

## Author

Hashim Waleed Dixon