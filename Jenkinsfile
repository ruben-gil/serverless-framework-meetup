
pipeline {
    agent any

    stage ('Unit testing') {
          steps {
              script {
                  '''
                      coverage run test_users.py
                      coverage report
                  '''
              }
          }
    }
    stages {
        stage ('Deploy') {
            steps {
                script {
                    sh "sls deploy --stage $BRANCH_NAME"
                }
            }
        }
    }
}