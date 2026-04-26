pipeline {
    agent any

    environment {
        IMAGE_NAME = "recipe-book"
        CONTAINER_NAME = "recipe-book-app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Verify') {
            steps {
                echo 'Running unit tests...'
                sh 'docker run --rm ${IMAGE_NAME}:latest python -m pytest tests/ -v'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Stopping any existing container...'
                sh 'docker stop ${CONTAINER_NAME} || true'
                sh 'docker rm ${CONTAINER_NAME} || true'

                echo 'Starting updated container...'
                sh 'docker run -d --name ${CONTAINER_NAME} -p 5000:5000 -e MONGO_URI=mongodb://mongo:27017/ ${IMAGE_NAME}:latest'

                echo 'App is live at http://localhost:5000'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully. Recipe Book is running!'
        }
        failure {
            echo 'Pipeline failed. Check the logs above for details.'
        }
    }
}
