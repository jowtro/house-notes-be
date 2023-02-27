pipeline { 
    agent any 
    environment {
        PORT_APP = '8091'
        APP_SETTINGS = "${APP_SETTINGS}"
    }
    options {
        timeout(time: 1, unit: 'HOURS')
    }
    triggers {
        pollSCM('H/5 * * * *')
    }
    stages { 
        stage('Setup') {
            steps {
                script {
                    // Get latest git tag
                    echo "Build"
                    sh 'docker compose down'
                }
            }
        }
        stage('Build') {
          
            steps {
                script {
                    // Get latest git tag
                    echo "Build"
                    sh "docker compose build --no-cache --build-arg PORT_APP=${PORT_APP}"
                }
            }
        }
        stage ('Deploy') { 
            steps {
                script {
                        // Start the containers with the JWT_SECRET environment variable
                        // Deploy the Docker image to the Minikube Kubernetes cluster
                        echo "Deploying"
                        withCredentials([
                            string(credentialsId: 'JWT_HOUSE_BE', variable: 'JWT_SECRET_KEY'), 
                            string(credentialsId: 'USER_TEST_HOUSE_BE', variable: 'USER_TEST'),
                            string(credentialsId: 'PASS_TEST_HOUSE_BE', variable: 'PASS_TEST'),
                            string(credentialsId: 'PGSQL_NOTED', variable: 'DATABASE_URL')
                            
                            ]) {
                            sh ('docker compose up -d')
                    }
                }
            }
        }
    }           
}
