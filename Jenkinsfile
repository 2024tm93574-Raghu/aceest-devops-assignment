pipeline {
    agent any

    environment {
        IMAGE_NAME = "aceest-fitness"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '>>> Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '>>> Installing Python dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo '>>> Running flake8 syntax check...'
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    flake8 app.py routes/ models/ --max-line-length=120 --ignore=E501,W503 || true
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo '>>> Running Pytest unit tests...'
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/test_app.py -v --tb=short
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo '>>> Building Docker image...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }

        stage('Verify Build') {
            steps {
                echo '>>> Verifying Docker image...'
                sh "docker images ${IMAGE_NAME}"
            }
        }
    }

    post {
        success {
            echo '✅ BUILD SUCCESSFUL — ACEest image is ready.'
        }
        failure {
            echo '❌ BUILD FAILED — Check the logs above.'
        }
        always {
            echo '>>> Cleaning up workspace...'
            cleanWs()
        }
    }
}