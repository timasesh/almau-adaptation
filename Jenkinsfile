pipeline {
    agent {label 'deployment_2'}

    environment {
        DOCKER_REGISTRY = "registry.example.com"   // твой Docker Registry
        DOCKER_IMAGE = "adaptation"
        DOCKER_TAG = "latest"
        CONTAINER_NAME = "adaptation_app"
        ENV_FILE = ".env"
        APP_PORT = "8000"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
         stage('Inject .env') {
    steps {
        withCredentials([file(credentialsId: 'adaptation-env', variable: 'ENV_FILE')]) {
            sh '''
            echo "⚡ Injecting .env from Jenkins Secret File"
            rm .env || true
            cp $ENV_FILE .env
            ls -la .env
            '''
        }
    }
}



        stage('Build Docker Image') {
            steps {
                sh '''
                docker build  --no-cache -t $DOCKER_IMAGE:$DOCKER_TAG .
                '''
            }
        }



        stage('Deploy Container') {
            steps {
                sh '''
                echo "⚡ Stopping old container if exists"
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true

                echo "⚡ Running new container"
                docker run -d --name $CONTAINER_NAME -p $APP_PORT:8000 --env-file .env $DOCKER_IMAGE:$DOCKER_TAG
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Deployment failed!'
        }
    }
}
