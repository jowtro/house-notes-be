pipeline { 
    agent any 
    options {
        timeout(time: 1, unit: 'HOURS')
    }
    triggers {
        pollSCM('H/5 * * * *')
    }
    environment {
        appName = "house-notes-be"
        registry = "localhost:5000"
    }
    stages { 
        stage('Build') {
            steps {
                script {
                    // Get latest git tag
                    sh "git rev-parse --short HEAD > commit-id"
                    tag = readFile('commit-id').replace("\n", "").replace("\r", "")
                    registryHost = "${registry}/"
                    imageName = "$registryHost${appName}:${tag}"
                    echo "ImageName -> $imageName"
                    // Build Docker image
                    app_image = docker.build("${imageName}") // assign customImage here
                    // Push Docker image to registry
                    echo "Build image done!"
                    
                    
                }
            }
        }
        stage("Push") {
            steps {
                script {
                    //jowtro_registry is the credentials got from jenkins
                    docker.withRegistry('http://${registry}','jowtro_registry') {
                    echo "Pushing to registry..."
                        app_image.push()
                    }
                    echo "Pushing to registry done!"

                }
            }
        }
        stage ('Deploy') { 
            steps {
                script {
                    // Deploy the Docker image to the Minikube Kubernetes cluster
                    echo "Deploying"
                    sh 'kubectl apply -f deployment.yml'
                    sh 'kubectl apply -f service.yml'
                    sh "kubectl set image deployment/${appName}-deployment ${appName}-container=${imageName}"
                    sh "kubectl rollout status deployment/${appName}-deployment --timeout=5m"
                }
            }
        }
        stage ('Monitor') { 
              steps {
                // Monitor the deployed application
                sh 'kubectl get pods'
                sh 'kubectl get svc'
            }
        }
 
    }           
 }
