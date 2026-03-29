# ACEest Fitness & Gym – DevOps CI/CD Project

## Introduction

This project is a Flask-based fitness and gym management application developed as part of a DevOps assignment. The system helps manage clients, track workouts, monitor progress, and store body metrics.

The main goal of this project is not only to build a working application, but also to implement a complete DevOps pipeline using Git, Docker, GitHub Actions, and Jenkins.

---

## Project Structure

The project is organized into multiple folders for better clarity and modular design:

* `app.py` – Main Flask application
* `models/db.py` – Database initialization and schema
* `routes/` – Contains route files for client and analytics logic
* `templates/` – HTML pages for UI
* `static/` – CSS styling
* `tests/` – Pytest test cases
* `Dockerfile` – Instructions to build Docker image
* `Jenkinsfile` – Jenkins pipeline configuration
* `.github/workflows/main.yml` – GitHub Actions pipeline

---

## How to Run the Application Locally

1. Clone the repository:

   ```
   git clone https://github.com/<your-username>/aceest-fitness.git
   cd aceest-fitness
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate   (on Windows)
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:

   ```
   python app.py
   ```

5. Open in browser:

   ```
   http://localhost:5000
   ```

Default login credentials:

* Username: admin
* Password: admin

---

## Running Tests

To run tests manually:

```
pytest
```

The test cases verify:

* Application health endpoint
* Dashboard loading
* Calories API functionality

---

## Docker Setup

To build and run the application using Docker:

1. Build the image:

   ```
   docker build -t aceest-fitness .
   ```

2. Run the container:

   ```
   docker run -p 5000:5000 aceest-fitness
   ```

---

## GitHub Actions (CI Pipeline)

The CI pipeline is configured using GitHub Actions.

It is triggered on every push and pull request to the main branch.

The pipeline performs the following steps:

1. Installs dependencies
2. Runs pytest
3. Builds the Docker image

This ensures that the code is always tested and build-ready.

---

## Jenkins Pipeline

Jenkins is used as the BUILD stage in the pipeline.

The Jenkins pipeline performs:

* Code checkout from GitHub
* Dependency installation
* Running tests using pytest
* Building the Docker image

This acts as an additional validation layer before deployment.

---

## Application Features

The application provides the following features:

* Add and manage client profiles
* Automatically calculate calorie requirements
* Log workouts and track duration
* Record weekly progress and adherence
* Store body metrics such as weight, waist, and body fat
* Generate progress charts
* Simple login system using session management
* API endpoint for calorie recommendation

---

## DevOps Implementation

This project demonstrates the following DevOps concepts:

* Version control using Git and GitHub
* Automated testing using Pytest
* Containerization using Docker
* Continuous Integration using GitHub Actions
* Build automation using Jenkins

---

## Conclusion

This project shows how a simple Flask application can be integrated with modern DevOps tools to create a complete CI/CD workflow. It ensures code quality, consistency across environments, and automated build processes.

---
