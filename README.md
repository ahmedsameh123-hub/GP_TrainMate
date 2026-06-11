# TrainMate

TrainMate is a complete fitness application composed of three main parts:

1. `ai/` - AI utilities and exercise model support.
2. `trainmate_backend/` - FastAPI backend server.
3. `trainmate_app/` - Flutter client application.

## Overview

- Backend: **FastAPI** with JWT authentication, default SQLite database, and optional ML support.
- Frontend: **Flutter** application for mobile and desktop.
- Communication: The Flutter app connects to the backend API via HTTP.
- ML model: Exercise classification can run on the backend if model files are available.

## Project structure

- `ai/`
  - Python code for training and extracting pose features.
  - Typically contains model weights (`.h5`) and `joblib` files needed for exercise classification.
- `trainmate_backend/`
  - FastAPI backend server.
  - Environment files and API router modules in `app/`.
- `trainmate_app/`
  - Flutter application.
  - Includes screens for authentication, settings, workout flow, and more.

## Backend setup

### 1. Open PowerShell

### 2. Change to the backend folder

```powershell
cd "c:\Users\HUAWEI\OneDrive\Desktop\PP\trainmate_backend"
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If the virtual environment does not exist, create it first:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 5. Install ML-related dependencies

```powershell
pip install "numpy>=1.23,<2" mediapipe==0.10.9 opencv-python-headless
```

### 6. Create and configure `.env`

Copy `.env.example` to `.env` and update:

- `JWT_SECRET_KEY` with a secure random string.
- `DATABASE_URL` (default is `sqlite:///./trainmate.db`).
- `GROQ_API_KEY` if you want chat/AI features.
- Email settings (`SMTP_*` or `RESEND_API_KEY`) for real verification emails.
- `ML_MODELS_DIR` if you want to store ML model files outside `ai/models/`.

### 7. Start the backend

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. Verify the backend is running

Open a browser and visit:

```text
http://127.0.0.1:8000/api/health
```

If you see JSON containing `status: ok`, the backend is running.

## Flutter app setup

### 1. Open a new PowerShell window

### 2. Change to the Flutter app folder

```powershell
cd "c:\Users\HUAWEI\OneDrive\Desktop\PP\trainmate_app"
```

### 3. Install Flutter packages

```powershell
flutter pub get
```

### 4. Launch the emulator

```powershell
flutter emulators --launch Medium_Phone_API_36.1
```

### 5. Run the app

```powershell
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

> Note: Android emulator uses `10.0.2.2` to access the local machine.

### 6. Run on desktop or iOS simulator

```powershell
flutter run --dart-define=API_BASE_URL=http://127.0.0.1:8000
```

## Why this API address matters

- Android emulator cannot access `127.0.0.1` on the host directly.
- Use `10.0.2.2` so the emulator can reach the backend running on your computer.

## App-specific details

### API base URL configuration

The app chooses the API base URL from:

1. `AppConstants.devApiBaseUrlOverride` in `trainmate_app/lib/core/constants.dart`
2. `--dart-define=API_BASE_URL=...`
3. Default fallback values in the code, such as:
   - `http://10.0.2.2:8000`
   - `http://127.0.0.1:8000`
   - `http://localhost:8000`

### Request service logic

- `trainmate_app/lib/services/api_service.dart` handles API requests.
- It sends `Bearer` JWT authorization automatically after login.

### Main app routes

- `lib/main.dart` is the app entry point.
- `lib/routes/app_routes.dart` defines navigation routes.
- `lib/services/*` contains networking and storage services.

## Main backend APIs

### Authentication

- `POST /api/auth/register` - register a new user.
- `POST /api/auth/login` - login and get a JWT.
- `POST /api/auth/verify-email` - verify email.
- `POST /api/auth/forgot-password` - request password reset.
- `POST /api/auth/reset-password` - reset password.

### User data

- `GET /api/users/me` - get current user profile.
- `PATCH /api/users/me/profile` - update profile data.
- `PATCH /api/users/me/account` - update account information.
- `PATCH /api/users/me/plan` - update workout plan.

### Workout and AI

- `POST /api/workouts` - create a workout session.
- `GET /api/workouts` - list workout sessions.
- `GET /api/ml/status` - check ML model availability.
- `POST /api/ml/classify` - classify pose data with ML.

## AI model area

- The backend ML router is at `trainmate_backend/app/routers/ml.py`.
- If using the Keras model, place these files in `ai/models/` or the path defined in `ML_MODELS_DIR`:
  - `final_forthesis_bidirectionallstm_and_encoders_exercise_classifier_model.h5`
  - `thesis_bidirectionallstm_scaler.pkl`
  - `thesis_bidirectionallstm_label_encoder.pkl`

## Full run workflow

Run the project from your laptop using the emulator:

1. Start the backend:
   ```powershell
   cd "c:\Users\HUAWEI\OneDrive\Desktop\PP\trainmate_backend"
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pip install "numpy>=1.23,<2" mediapipe==0.10.9 opencv-python-headless
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
2. Start the Flutter app:
   ```powershell
   cd "c:\Users\HUAWEI\OneDrive\Desktop\PP\trainmate_app"
   flutter pub get
   flutter emulators --launch Medium_Phone_API_36.1
   flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
   ```

## Common issues and fixes

- If the app cannot connect:
  - Make sure backend is running at `http://127.0.0.1:8000`.
  - Use `http://10.0.2.2:8000` on Android emulator.
  - Disable firewall or allow access if needed.

- If dependency installation fails:
  - Ensure `.venv\Scripts\Activate.ps1` is active.
  - Verify your Python version is compatible.
  - Re-run the ML installs if `mediapipe` or `opencv-python-headless` fail.

- If Flutter errors appear:
  - Run `flutter pub get` first.
  - Check `trainmate_app/lib/core/constants.dart` for the API default URL.
  - Run with `--dart-define=API_BASE_URL=http://10.0.2.2:8000` explicitly.

## Additional documentation

- `trainmate_backend/BACKEND_DOCUMENTATION.md`
- `trainmate_backend/BACKEND_DOCUMENTATION_AR.md`
- `trainmate_backend/docs/BACKEND_DOCUMENTATION.html`

## Notes

This README covers the full project setup from backend to Flutter client. If you want, I can add a detailed debug section for the specific `flutter run` error you are seeing.
