# ACEest Fitness & Gym — DevOps CI/CD Project

**Student:** Raghu Rapole | **ID:** 2024TM93574
**Course:** Introduction to DevOps (CSIZG514/SEZG514) | S1-25

---

## Assignment 1 — What Was Built

A complete CI/CD pipeline for a Flask-based gym management application.

### Application Features
- Add and manage client profiles with calorie calculation
- Log workouts and track duration
- Record weekly progress and adherence percentages
- Store body metrics (weight, waist, body fat)
- Generate progress charts using matplotlib
- AI workout program generator
- Session-based login system (default: admin / admin)
- REST API endpoint for calorie recommendations

### Assignment 1 Pipeline
| Tool | Role |
|------|------|
| Git + GitHub | Version control and remote repository |
| Pytest | Automated unit testing (health, auth, calories API) |
| Docker | Containerize the Flask application |
| GitHub Actions | CI pipeline: install → lint → test → docker build |
| Jenkins | Secondary BUILD stage: checkout → setup → lint → test → docker build |

---

## Assignment 2 — What Was Extended

Building on Assignment 1, the pipeline now includes SonarQube code quality scanning, Docker Hub image publishing, and Kubernetes deployment with 5 deployment strategies.

### New Components Added
| Component | Description |
|-----------|-------------|
| `sonar-project.properties` | SonarQube static analysis configuration |
| `k8s/deployment.yaml` | Kubernetes Rolling Update deployment (3 replicas) |
| `k8s/service.yaml` | LoadBalancer service (port 80 → Flask 5000) |
| `k8s/blue-green.yaml` | Blue-Green: instant traffic switching between versions |
| `k8s/canary.yaml` | Canary: 10% traffic to new version, 90% stable |
| `k8s/shadow.yaml` | Shadow: mirror live traffic to new version silently |
| `k8s/ab-testing.yaml` | A/B Testing: 50/50 split between two variants |
| `Jenkinsfile` (updated) | 7 stages: added SonarQube + Docker Push + K8s Deploy |
| `.github/workflows/main.yml` (updated) | Added Docker Hub push job after tests pass |

### Assignment 2 Pipeline (8 Stages)
```
Code Push → GitHub
    → Jenkins triggers:
        1. Checkout
        2. Python Setup
        3. Lint (flake8)
        4. Unit Tests (pytest + coverage XML)
        5. SonarQube Scan (bugs, vulnerabilities, code smells)
        6. Docker Build + Push to Docker Hub
        7. Kubernetes Deploy (Rolling Update)
    → On failure: auto kubectl rollout undo
```

---

## Project Structure

```
aceest-devops-assignment/
├── app.py                        # Main Flask application
├── models/
│   └── db.py                     # SQLite database schema
├── routes/
│   ├── client_routes.py          # Dashboard, delete client
│   └── analytic_routes.py        # Progress, workouts, metrics
├── templates/                    # HTML pages
│   ├── login.html, dashboard.html, index.html
│   ├── client_plan.html, ai_program.html, chart.html
│   ├── progress.html, workouts.html, metrics.html
├── static/
│   └── styles.css                # Dark theme styling
├── tests/
│   └── test_app.py               # Pytest test suite
├── k8s/                          # Kubernetes manifests (Assignment 2)
│   ├── deployment.yaml           # Rolling Update strategy
│   ├── service.yaml              # LoadBalancer service
│   ├── blue-green.yaml           # Blue-Green strategy
│   ├── canary.yaml               # Canary Release strategy
│   ├── shadow.yaml               # Shadow deployment
│   └── ab-testing.yaml           # A/B Testing strategy
├── Dockerfile                    # Container build instructions
├── Jenkinsfile                   # Jenkins 7-stage pipeline
├── sonar-project.properties      # SonarQube configuration
├── requirements.txt              # Python dependencies
└── .github/workflows/main.yml    # GitHub Actions CI/CD
```

---

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/2024tm93574-Raghu/aceest-devops-assignment.git
cd aceest-devops-assignment

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. Open browser
# http://localhost:5000
# Login: admin / admin
```

---

## Running Tests

```bash
# Run all tests
pytest tests/test_app.py -v

# Run with coverage report
pytest tests/test_app.py -v --cov=. --cov-report=xml
```

Tests cover:
- `/health` endpoint returns `{"status": "ok"}`
- Dashboard redirects to login when not authenticated
- Login page loads correctly
- Invalid credentials stay on login page
- `/recommend_calories` returns correct values for Fat Loss, Muscle Gain, Beginner

---

## Docker

```bash
# Build image
docker build -t aceest-fitness .

# Run container
docker run -p 5000:5000 aceest-fitness

# Pull from Docker Hub
docker pull 2024tm93574raghu/aceest-fitness:latest

# Docker Hub repository
# https://hub.docker.com/r/2024tm93574raghu/aceest-fitness
```

---

## SonarQube (Assignment 2)

```bash
# Start SonarQube (Docker required)
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community

# Open: http://localhost:9000  (login: admin / admin)
# Create project with key: aceest-fitness
# Generate a token, then run:

sonar-scanner \
  -Dsonar.projectKey=aceest-fitness \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN_HERE
```

---

## Kubernetes Deployment (Assignment 2)

```bash
# Prerequisites: Install Minikube + kubectl

# Start Minikube
minikube start

# Strategy 1: Rolling Update (default, zero downtime)
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service aceest-fitness-service --url   # Get access URL

# Strategy 2: Blue-Green (instant traffic switch)
kubectl apply -f k8s/blue-green.yaml

# Strategy 3: Canary (10% traffic to new version)
kubectl apply -f k8s/canary.yaml

# Strategy 4: Shadow (mirror traffic, no user impact)
kubectl apply -f k8s/shadow.yaml

# Strategy 5: A/B Testing (50/50 user split)
kubectl apply -f k8s/ab-testing.yaml

# Rollback (emergency)
kubectl rollout undo deployment/aceest-fitness

# Check pod status
kubectl get pods
```

---

## Jenkins Pipeline

The Jenkins pipeline reads the `Jenkinsfile` from this repository via SCM.

**Assignment 1 stages:** Checkout → Setup → Lint → Unit Tests → Docker Build

**Assignment 2 stages (additional):**
- **Stage 5:** SonarQube static analysis (requires SonarQube server configured in Jenkins)
- **Stage 6:** Build Docker image + push to Docker Hub (requires `dockerhub-creds` credential in Jenkins)
- **Stage 7:** Deploy to Kubernetes via `kubectl` commands

On pipeline failure, the `post { failure }` block automatically runs `kubectl rollout undo` to revert to the last stable version.

---

## GitHub Actions

Triggered on every push and pull request to `main`.

**Job 1 — test:** Install → Lint → Pytest (runs on all pushes and PRs)

**Job 2 — docker:** Build Docker image + Push to Docker Hub (runs only after test job passes, only on push to main)

Docker Hub credentials must be added to GitHub Secrets as:
- `DOCKER_USERNAME` = `2024tm93574raghu`
- `DOCKER_PASSWORD` = your Docker Hub password or access token

---

## DevOps Concepts Demonstrated

| Concept | Tool Used |
|---------|-----------|
| Version Control | Git + GitHub |
| Automated Testing | Pytest |
| Code Quality | SonarQube |
| Containerization | Docker |
| Image Registry | Docker Hub |
| CI Pipeline | GitHub Actions |
| Build Automation | Jenkins |
| Container Orchestration | Kubernetes (Minikube) |
| Deployment Strategies | Rolling, Blue-Green, Canary, Shadow, A/B |
| Auto Rollback | `kubectl rollout undo` |

---