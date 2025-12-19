**cis-proctoring — Knowledge Transfer (KT)

Overview
- Purpose: Online proctoring platform combining Django web app, real-time channels, face/eye detection, screen recording and AI modules for exam monitoring.
- Main languages: Python (Django), some C rendering helper in `image_ai/asset`.

Repository layout (high level)
- `manage.py` — Django CLI.
- `proctoring/` — Django project settings, ASGI/WGSI entrypoints.
- `exams/` — core app: models, views, admin, exam logic.
- `image_ai/` — computer-vision modules: face detection, landmarks, pose, spoofing.
- `screen_recorder/` — screen capture endpoints/UI.
- `users/` — user management.
- `media/` — runtime media (captured images, chunk_vid).
- `weights/` — ML model files used by `image_ai`.
- `Dockerfile`, `docker-compose.yml` — containerized deployment (optional).

Key files to know
- [proctoring/settings.py](proctoring/settings.py) — environment-driven settings (DB, Redis, channels).
- [image_ai/face_detector.py](image_ai/face_detector.py) and [image_ai/face_landmarks.py](image_ai/face_landmarks.py) — core CV logic.
- [exams/models.py](exams/models.py) — exam, question and answer models.
- `requirements.txt` — Python dependency list (contains heavy ML packages).

Prerequisites (local, Linux)
- System packages: `build-essential`, `cmake`, `python3-dev`, `libopenblas-dev`, `liblapack-dev`, `libx11-dev`, `libgtk-3-dev`, `libgl1-mesa-glx`, `portaudio19-dev`, `libatlas-base-dev`.
- Python 3.10 recommended (Dockerfile targets 3.10.12).
- Redis (if using Channels/real-time features).
- (Optional) Conda if building `dlib` via conda is preferred.

Local setup (no Docker)
1. Create & activate virtualenv
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

2. Install system deps (one-liner example)
```bash
sudo apt update
sudo apt install -y build-essential cmake python3-dev libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev libgl1-mesa-glx portaudio19-dev libatlas-base-dev
```

3. Install `dlib` (often the trickiest):
```bash
pip install dlib==19.24.0
# If pip build fails, use conda:
# conda create -n proctor python=3.10
# conda activate proctor
# conda install -c conda-forge dlib
```

4. Install Python dependencies
```bash
pip install -r requirements.txt
```
Notes: `requirements.txt` includes multiple TensorFlow variants and other heavy packages — for CPU-only systems use `tensorflow-cpu` and remove conflicting TF packages if needed.

5. Database & initial data
```bash
python manage.py migrate
python manage.py createsuperuser
# optional fixtures
python manage.py loaddata initial_data 2>/dev/null || true
```

6. Prepare media/static
```bash
mkdir -p media/captured_images media/chunk_vid
python manage.py collectstatic --noinput
```

7. Run dev server
- Simple Django runserver:
```bash
python manage.py runserver 0.0.0.0:8000
```
- For Channels/ASGI (recommended for real-time features):
```bash
# Ensure Redis running on default or configured host
daphne proctoring.asgi:application --port 8000
```

Running with Docker (short notes)
- Build image (from repo root): `docker build -t cis-proctoring .`
- Or use `docker-compose up --build` (check `docker-compose.yml` for env vars)

Key runtime considerations
- `weights/` directory must contain required model files used by `image_ai` modules. If models are missing, the CV modules will error.
- Redis: required by `channels-redis` for WebSocket layer; start with `redis-server` locally or run a Redis container.
- Media storage: in production use a persistent volume or object storage (S3).

Important modules & responsibilities
- `exams/` — exam lifecycle, models, scoring, captured answers.
- `image_ai/` — detection and anti-spoofing logic: responsible for face auth, landmarks, pose, spoof detection.
- `screen_recorder/` — handles screen capture API and storage of recorded chunks.
- `users/` — user profiles and authentication.
- `service/` — lower-level helpers for TFLite and rendering.

How to add a new feature (high level)
1. Create/modify models in the appropriate app.
2. Run `python manage.py makemigrations <app>` and `migrate`.
3. Add views and templates under the app; wire URLs in app `urls.py` and include in project `proctoring/urls.py`.
4. Add tests in the app's `tests.py` and run `pytest` or `python manage.py test`.

Debugging common issues
- dlib build errors: ensure `cmake`, `python3-dev` and compilers are installed; try conda prebuilt package.
- Missing model files: verify `weights/` exists and files referenced in code match filenames.
- Channels/WS failures: check `REDIS_URL` or `CHANNEL_LAYERS` in settings and ensure Redis is reachable.
- Heavy installs (TensorFlow): on low-memory / constrained systems, install only needed TF packages.

Useful commands summary
- Create venv: `python3 -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -r requirements.txt`
- Migrate DB: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Collect static: `python manage.py collectstatic --noinput`
- Run server (dev): `python manage.py runserver`
- Run ASGI: `daphne proctoring.asgi:application --port 8000`

Next steps & suggestions
- Trim `requirements.txt` to a `requirements-local.txt` removing unused TF variants for faster installs.
- Add an `.env.example` with required env vars (DB, REDIS_URL, SECRET_KEY placeholder).
- Add a short `dev-setup.sh` script automating the venv and install steps.

Contacts & ownership
- Current repo maintainer: check `README.md` or project owners; if unknown, add owner contact info here.

If you want, I can:
- produce a `requirements-local.txt` trimmed for local/dev use,
- add a `dev-setup.sh` to automate the steps above, or
- run the install commands here and verify the server starts (I will need permission to run them).
