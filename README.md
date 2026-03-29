# ACEest Fitness & Gym — DevOps CI/CD Pipeline

> A Flask-based fitness management system with automated CI/CD using GitHub Actions and Jenkins.

---

## Project Structure

aceest/
├── app.py                        # Main Flask application
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container build instructions
├── Jenkinsfile                   # Jenkins BUILD pipeline
├── .github/
│   └── workflows/
│       └── main.yml              # GitHub Actions CI/CD pipeline
├── models/
│   └── db.py                     # SQLite database initialization
├── routes/
│   ├── client_routes.py          # Client management endpoints
│   └── analytic_routes.py        # Progress, workouts & metrics endpoints
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── login.html
│   ├── progress.html
│   ├── workouts.html
│   ├── metrics.html
│   ├── chart.html
|   ├── ai_program.html
|   └── client_plan.html
├── static/
│   └── styles.css
└── tests/
    └── test_app.py               # Pytest test suite

---

## Local Setup & Execution

### Prerequisites
- Python 3.11+
- Docker (for containerized runs)
- Git

### 1. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.
Default login: **admin / admin**

---

##  Running with Docker

### Build the Image
```bash
docker build -t aceest-fitness:latest .
```

### Run the Container
```bash
docker run -p 5000:5000 aceest-fitness:latest
```

---

##  Running Tests Manually

### Without Docker
```bash
pip install pytest
python -m pytest tests/test_app.py -v
```

### Inside Docker
```bash
docker run --rm aceest-fitness:latest python -m pytest tests/test_app.py -v
```

### Test Coverage
| Test | Route | Expected |
|---|---|---|
| `test_health` | `GET /health` | 200 OK |
| `test_dashboard` | `GET /dashboard` | 200 OK (redirects to login) |
| `test_calories_api` | `POST /recommend_calories` | 200 + JSON |

---

##  GitHub Actions — CI/CD Pipeline

**File:** `.github/workflows/main.yml`

**Triggered on:** Every `push` or `pull_request` to `main`

### Pipeline Stages

```
Push to GitHub
      │
      ▼
┌─────────────┐
│  1. Lint    │  flake8 syntax & style check
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  2. Docker Build │  Build Docker image from Dockerfile
└────────┬─────────┘
         │
         ▼
┌───────────────────────┐
│  3. Pytest (in Docker)│  Run full test suite inside the container
└───────────────────────┘
```

Each job depends on the previous — if lint fails, Docker build is skipped, and so on.

---

##  Jenkins — BUILD Stage

**File:** `Jenkinsfile`

Jenkins handles the primary BUILD and quality gate phase.

### Jenkins Setup Steps

1. **Install Jenkins** (locally or via Docker):
   ```bash
   docker run -p 8080:8080 jenkins/jenkins:lts
   ```

2. **Install plugins:** Git, Pipeline, Docker Pipeline

3. **Create a new Pipeline job:**
   - Source: Pipeline script from SCM
   - SCM: Git → your GitHub repo URL
   - Branch: `main`
   - Script path: `Jenkinsfile`

4. **Trigger a build** — Jenkins will:

### Jenkins Pipeline Stages

| Stage | Description |
|---|---|
| Checkout | Pulls latest code from GitHub |
| Setup Python | Creates venv and installs dependencies |
| Lint | Runs flake8 syntax checks |
| Unit Tests | Executes `pytest` test suite |
| Docker Build | Builds and tags the Docker image |
| Verify Build | Confirms image exists locally |

---

##  Application Features

- **Client Management** — Add, view, and delete client profiles
- **Calorie Estimation** — Auto-calculated based on weight × program factor
- **Workout Logging** — Log workout type and duration per client
- **Progress Tracking** — Weekly adherence tracking with chart visualization
- **Body Metrics** — Track weight, waist, and body fat over time
- **REST API** — `/recommend_calories` JSON endpoint
- **Authentication** — Session-based login (admin/admin by default)
