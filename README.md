# StartPitch API

Flask backend API for StartPitch — a platform connecting startup founders with investors and mentors. Handles auth, startup/pitch submissions, AI-assisted evaluations, investor matching, mentor bookings, deal rooms, messaging, and notifications.

> **Note:** Data models (users, startups, pitches, matches, etc.) are currently held in in-memory Python dicts/lists inside each route module — there is no database wired up yet. All data resets when the server restarts.

## Tech stack

- Python 3.12
- Flask 3
- flask-jwt-extended (auth)
- flask-bcrypt (password hashing)
- flask-cors
- gunicorn (production server)

## Getting started

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

Run the development server:

```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000`.

For production, the `Procfile` runs it via gunicorn:

```bash
gunicorn run:app
```

### Environment variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `JWT_SECRET_KEY` | Secret used to sign JWTs | `jwt-dev-secret` |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token lifetime (seconds) | `1800` |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh token lifetime (seconds) | `604800` |

## Authentication

Most endpoints require a Bearer JWT access token, obtained from `/api/v1/auth/login` or `/api/v1/auth/register`:

```
Authorization: Bearer <access_token>
```

Endpoints under `/api/v1/admin` additionally require the JWT's `role` claim to be `admin`.

## Health check

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Liveness check, returns `{"status": "ok"}` |

## API Endpoints

All endpoints below are prefixed with `/api/v1` unless noted otherwise. 🔒 = requires `Authorization: Bearer <token>`. 🔒admin = requires an admin role.

### Auth (`/api/v1/auth`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user (`email`, `password`, `role`) |
| POST | `/auth/login` | Log in with `email`/`password`, returns access + refresh tokens |
| POST | `/auth/oauth/google` | Google OAuth login (stub) |
| POST | `/auth/oauth/linkedin` | LinkedIn OAuth login (stub) |
| POST | `/auth/refresh` 🔒 (refresh token) | Exchange a refresh token for a new token pair |

### Users (`/api/v1/users`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/me` 🔒 | Get the current authenticated user |
| PATCH | `/users/me` 🔒 | Update the current user's profile |
| GET | `/users/<user_id>/profile-completeness` 🔒 | Get profile completeness score (0–100) |

### Startups (`/api/v1/startups`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/startups` 🔒 | Create a startup |
| GET | `/startups/<startup_id>` 🔒 | Get a startup by ID |
| PATCH | `/startups/<startup_id>` 🔒 | Update a startup |

### Pitches (`/api/v1/pitches`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/pitches` 🔒 | Create a pitch |
| GET | `/pitches` 🔒 | List pitches (filter by `?startup_id=`, `?visibility=`) |
| GET | `/pitches/<pitch_id>` 🔒 | Get a pitch by ID |
| POST | `/pitches/<pitch_id>/versions` 🔒 | Add a new version to a pitch (`content_url`) |
| GET | `/pitches/<pitch_id>/versions` 🔒 | List versions of a pitch |
| GET | `/pitches/<pitch_id>/versions/<version_id>` 🔒 | Get a specific pitch version |
| GET | `/pitches/<pitch_id>/versions/<version_id>/status` 🔒 | Get processing status of a version |
| GET | `/pitches/<pitch_id>/score-history` 🔒 | Get score history across versions |

### Evaluations (`/api/v1/evaluations`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/evaluations` 🔒 | Queue an AI evaluation job for a `pitch_version_id` |
| GET | `/evaluations/jobs/<job_id>` 🔒 | Get status/result of an evaluation job |
| GET | `/evaluations/<pitch_version_id>` 🔒 | Get the completed evaluation for a pitch version |
| POST | `/evaluations/<evaluation_id>/override` 🔒 | Manually override an evaluation's result |

### Matching (`/api/v1`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/thesis` 🔒 | Create/update an investor's thesis |
| GET | `/thesis/<investor_id>` 🔒 | Get an investor's thesis |
| GET | `/matches/for-investor/<investor_id>` 🔒 | List matches for an investor |
| GET | `/matches/for-startup/<startup_id>` 🔒 | List matches for a startup |
| GET | `/matches/<match_id>/rationale` 🔒 | Get the rationale behind a match |
| POST | `/matches/recompute` 🔒 | Recompute all startup ↔ investor thesis matches |

### Reputation (`/api/v1/reputation`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/reputation/<user_id>` 🔒 | Get a user's reputation score and ratings |
| POST | `/reputation/<user_id>/rate` 🔒 | Submit a rating for a user |
| GET | `/reputation/<user_id>/badges` 🔒 | Get badges earned by a user |

### Mentors (`/api/v1/mentors`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/mentors` 🔒 | List mentors (filter by `?expertise=`, `?availability=`) |
| GET | `/mentors/<mentor_id>` 🔒 | Get a mentor by ID |

### Bookings (`/api/v1/bookings`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/bookings` 🔒 | Create a mentor session booking |
| GET | `/bookings` 🔒 | List bookings (filter by `?user_id=`, `?role=`) |
| PATCH | `/bookings/<booking_id>` 🔒 | Update a booking |
| POST | `/bookings/<booking_id>/feedback` 🔒 | Submit feedback for a completed booking |

### Deal Rooms (`/api/v1/deal-rooms`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/deal-rooms` 🔒 | Create a deal room |
| GET | `/deal-rooms/<room_id>` 🔒 | Get a deal room |
| POST | `/deal-rooms/<room_id>/nda/sign` 🔒 | Sign the NDA for a deal room |
| POST | `/deal-rooms/<room_id>/documents` 🔒 | Add a document (`name`, `url`) |
| GET | `/deal-rooms/<room_id>/documents/<doc_id>/download` 🔒 | Get a document's download URL (logs access) |
| GET | `/deal-rooms/<room_id>/access-logs` 🔒 | Get the deal room's access log |

### Messages (`/api/v1/messages`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/messages` 🔒 | Send a message |
| GET | `/messages` 🔒 | List messages (filter by `?thread_with=`, `?deal_room_id=`) |

### Notifications (`/api/v1/notifications`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/notifications` 🔒 | List notifications for the current user |
| PATCH | `/notifications/<notification_id>/read` 🔒 | Mark a notification as read |

### Voice (`/api/v1/voice`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/voice/navigate` 🔒 | Voice-driven navigation intent (stub) |
| POST | `/voice/pitch-submission` 🔒 | Submit a pitch via voice transcript (stub) |

### Admin (`/api/v1/admin`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/admin/verifications/pending` 🔒admin | List pending user verifications |
| POST | `/admin/verifications/<user_id>/approve` 🔒admin | Approve a user's verification |
| GET | `/admin/audit-logs` 🔒admin | Get the admin audit log |
| POST | `/admin/moderation/<content_id>/flag` 🔒admin | Flag content for moderation |

## Project structure

```
app/
├── __init__.py          # App factory, blueprint registration
├── config.py            # Flask config from environment variables
├── extensions.py        # Shared extension instances (bcrypt, jwt, cors)
├── models/               # Data model definitions
├── routes/               # Blueprints, one per resource
└── services/              # Business logic (auth, matching, AI evaluation, notifications, etc.)
run.py                    # Entrypoint
Procfile                  # gunicorn start command for deployment
```
