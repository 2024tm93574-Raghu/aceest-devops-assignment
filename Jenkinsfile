// ================================================================
// ACEest Fitness & Gym — Jenkins Pipeline (Assignment 2 Version)
// Extends Assignment 1 (5 stages) with:
//   Stage 5: SonarQube Code Quality
//   Stage 6: Docker Hub Push
//   Stage 7: Kubernetes Deploy (Rolling Update)
//   + Automatic rollback on failure
// ================================================================

pipeline {
    agent any

    environment {
        DOCKER_USER  = "2024tm93574raghu"
        IMAGE_NAME   = "aceest-fitness"
        DOCKER_IMAGE = "${DOCKER_USER}/${IMAGE_NAME}"
        IMAGE_TAG    = "${BUILD_NUMBER}"
    }

    stages {

        // ── STAGE 1 (from Assignment 1) ──────────────────────────
        stage('1. Checkout') {
            steps {
                echo '>>> Pulling latest code from GitHub...'
                checkout scm
            }
        }

        // ── STAGE 2 (from Assignment 1) ──────────────────────────
        stage('2. Setup Python Environment') {
            steps {
                echo '>>> Installing Python dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install flake8 pytest-cov
                '''
            }
        }

        // ── STAGE 3 (from Assignment 1) ──────────────────────────
        stage('3. Lint') {
            steps {
                echo '>>> Running flake8 syntax check...'
                sh '''
                    . venv/bin/activate
                    flake8 app.py routes/ models/ \
                      --max-line-length=120 \
                      --ignore=E501,W503,E402,E401,E241,W292,F401 || true
                '''
            }
        }

        // ── STAGE 4 (from Assignment 1, enhanced with coverage) ──
        stage('4. Unit Tests') {
            steps {
                echo '>>> Running Pytest unit tests with coverage...'
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/test_app.py -v --tb=short \
                      --junitxml=test-results.xml \
                      --cov=. --cov-report=xml:coverage.xml || true
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        // ── STAGE 5 (NEW — Assignment 2) ─────────────────────────
        stage('5. SonarQube Analysis') {
            steps {
                echo '>>> Running SonarQube static code quality scan...'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=aceest-fitness \
                          -Dsonar.projectName="ACEest Fitness" \
                          -Dsonar.sources=. \
                          -Dsonar.language=py \
                          -Dsonar.python.version=3 \
                          -Dsonar.python.coverage.reportPaths=coverage.xml \
                          -Dsonar.exclusions=**/venv/**,**/__pycache__/**,**/tests/** \
                        || true
                    '''
                }
            }
        }

        // ── STAGE 6 (NEW — Assignment 2) ─────────────────────────
        stage('6. Build & Push Docker Image') {
            steps {
                echo ">>> Building Docker image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
                sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
                sh "docker tag  ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest"

                echo '>>> Pushing to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_U',
                    passwordVariable: 'DOCKER_P'
                )]) {
                    sh '''
                        echo $DOCKER_P | docker login -u $DOCKER_U --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        // ── STAGE 7 (NEW — Assignment 2) ─────────────────────────
        stage('7. Deploy to Kubernetes') {
            steps {
                echo '>>> Applying Kubernetes manifests (Rolling Update)...'
                sh '''
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl set image deployment/aceest-fitness \
                      aceest-fitness=${DOCKER_IMAGE}:${IMAGE_TAG}
                    kubectl rollout status deployment/aceest-fitness --timeout=120s
                '''
            }
        }

    }

    post {
        success {
            echo "✅ BUILD ${BUILD_NUMBER} PASSED — App deployed to Kubernetes!"
        }
        failure {
            echo "❌ BUILD ${BUILD_NUMBER} FAILED — Rolling back Kubernetes deployment..."
            sh 'kubectl rollout undo deployment/aceest-fitness || true'
        }
        always {
            echo '>>> Pipeline complete. Check Jenkins dashboard for full results.'
        }
    }
}
