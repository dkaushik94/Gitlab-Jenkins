// This is the Private Access token obtained in GitLab. Please replace this with the one you obtained in create_master_job.py. 
String private_token = "DjotJ94w7GRsRdU6eDWt"
// If the address of jenkins is different from this, please replace that too.
String ip = "http://172.17.0.3:80/"
        // We need to fetch URLs of all the repos in order to create a job for each of them
		def jdata = new groovy.json.JsonSlurper().parseText(new URL("http://172.17.0.3:80/api/v3/projects?private_token="+private_token).text)
		jdata.each {
			String repo_url = it.ssh_url_to_repo
          	repo_url = repo_url.replace("git@gitlab.example.com:",ip)
            String proj =  repo_url.substring(repo_url.lastIndexOf('/') + 1);
			String project_name =  proj[0..-5]
            job(project_name) {
                // Basic details of the job
                description('A job for the project: ' + project_name)
                displayName(project_name)

                // SCM details of the repo
                scm {
                    git {
                    branch('master')
                    remote { 
                        url(repo_url)
                        credentials('gitlab-root-user')
                    }
                    }
                }

                // Build steps
                steps {
                    gradle('check')
                    gradle {
                    tasks('clean')
                    tasks('build')
                    switches('--stacktrace')
                    switches('--debug')
                
                    }
                    
                }
                
                // Setting up Jacoco Code coverage
                publishers {
                    jacocoCodeCoverage {
                        execPattern '**/**.exec'
                        classPattern '**/classes'
                        sourcePattern '**/src/main/java'
                        exclusionPattern ''
                        inclusionPattern ''
                    }
                
                }
                
                // Setting up triggers for Gitlab
                triggers {
                        gitlabPush {
                            buildOnMergeRequestEvents(true)
                            buildOnPushEvents(true)
                        }
                    }
  
                authenticationToken('auhgtbereb675nksnwewrhbbe==')
  
            }
		}