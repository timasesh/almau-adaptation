pipeline {
    agent { label 'deployment_2' }

    environment {
        DOCKER_IMAGE   = "adaptation"
        DOCKER_TAG     = "latest"
        COMPOSE_FILE   = "docker-compose.yml"
        CONTAINER_NAME = "adaptation_web"
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
                    rm -f .env
                    cp $ENV_FILE .env
                    ls -la .env
                    '''
                }
            }
        }

        stage('Build & Up') {
            steps {
                sh '''
                echo "⚡ Building and starting containers via Compose"
                docker compose -f $COMPOSE_FILE down || true
                docker compose -f $COMPOSE_FILE build --no-cache
                docker compose -f $COMPOSE_FILE up -d --remove-orphans
                '''
            }
        }

        stage('Migrate & Collectstatic') {
            steps {
                sh '''
                echo "⚡ Running Django migrations and collectstatic"
                docker compose -f $COMPOSE_FILE exec -T web python manage.py migrate --noinput
                docker compose -f $COMPOSE_FILE exec -T web python manage.py collectstatic --noinput
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
