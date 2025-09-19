pipeline {
    agent {label 'deployment_2'}

    environment {
        DOCKER_REGISTRY = "registry.example.com"   // твой Docker Registry
        DOCKER_IMAGE = "almau-adaptation"
        DOCKER_TAG = "latest"
        CONTAINER_NAME = "almau_app"
        ENV_FILE = ".env"
        APP_PORT = "8006"
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
                    cp $ENV_FILE /tmp/$CONTAINER_NAME.env
                    '''
                }
            }
        }



        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG .
                '''
            }
        }

        stage('Push to Registry') {
            steps {
                sh '''
                echo "⚡ Login to registry"
                docker login $DOCKER_REGISTRY -u $DOCKER_USER -p $DOCKER_PASS
                docker push $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG
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
                docker run -d --name $CONTAINER_NAME \
                    -p $APP_PORT:8000 \
                    $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG
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
