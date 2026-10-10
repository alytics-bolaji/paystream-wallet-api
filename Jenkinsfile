pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { git branch: 'main', url: 'https://github.com/alytics-bolaji/paystream-wallet-api.git' }
    }
    stage('Lint') {
      steps { sh 'node --check wallet-api.js' }
    }
    stage('Test') {
      steps { sh 'bash tests.sh' }
    }
    
 }
}
