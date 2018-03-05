job('Test-Job-Complete') {
  
  description('A Test Job with entire Pipeline')
  displayName('Test-job-Complete')

  scm {
    git {
      branch('master')
      remote { 
        url('git@172.17.0.2:root/TokBox-BookStore.git')
        credentials('gitlab-root-user')
      }
    }
  }
  
  steps {
  	gradle('check')
    gradle {
      tasks('clean')
      tasks('build')
      switches('--stacktrace')
      switches('--debug')
  
  	}
    
  }
  
  publishers {
    jacocoCodeCoverage {
    	execPattern '**/**.exec'
      	classPattern '**/classes'
      	sourcePattern '**/src/main/java'
      	exclusionPattern ''
      	inclusionPattern ''
    }
  
  }
  
  triggers {
        gitlabPush {
            buildOnMergeRequestEvents(true)
            buildOnPushEvents(true)
        }
    }
  
  authenticationToken('auhgtbereb675nksnwewrhbbe==')
  
}
