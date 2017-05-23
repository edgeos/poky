node ('') {
    
    stage("SCM Checkout") {
        checkout scm
    }

    stage("Build") {
        sh '''
            ./build.sh
        '''
    }

}