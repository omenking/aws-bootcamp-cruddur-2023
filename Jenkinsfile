#!/usr/bin/env groovy

pipeline {
    agent none
    stages {
        stage('build') {
            steps {
                script {
                    echo "Building the application..."
                }
            }
        }
        stage('test') {
            steps {
                script {
                    echo "Testing the application..."
                }
            }
        }
        stage('deploy') {
            steps {
                script {
                    def dockerCmd = 'docker run -p 3000:3000 -d dannyboy01/frontend-react-js:latest'
                    sshagent(['ssh-key']) {
                        sh "ssh -o StrictHostKeyChecking=no ubuntu@100.25.153.24 ${dockerCmd}"
                    }
                }
            }
        }
    }
}
