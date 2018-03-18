import os
import sys
import traceback

# Method used to install any missing packages by running a bash command
def execute_bash(command):
    try:
        return os.system(command)
    except Exception:
        print(traceback.format_exc())


# Import python-jenkins package
try:
    import jenkins
except Exception:
    execute_bash("sudo pip3 install python-jenkins")


# This is the job XML for the Master job which contains the DSL script. When this job is created and built for first time, it will run
# the DSL script and generate jobs for each of the repo present in the gitlab repo.
job_xml = """ 

<project>
<actions/>
<description/>
<keepDependencies>false</keepDependencies>
<properties>
<com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.3">
<gitLabConnection>gitlab</gitLabConnection>
</com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
</properties>
<scm class="hudson.scm.NullSCM"/>
<canRoam>true</canRoam>
<disabled>false</disabled>
<blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
<blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
<triggers/>
<concurrentBuild>false</concurrentBuild>
<builders>
<javaposse.jobdsl.plugin.ExecuteDslScripts plugin="job-dsl@1.67">
<scriptText>
    // This is the Private Access token obtained in GitLab. Please replace this with the one you obtained in create_master_job.py. 
    String private_token = "sc24K_e5avo6QjiF7G7c"
    // If the address of jenkins is different from this, please replace that too.
    String ip = "http://172.17.0.2:80/"
        // We need to fetch URLs of all the repos in order to create a job for each of them
		def jdata = new groovy.json.JsonSlurper().parseText(new URL("http://172.17.0.2:80/api/v3/projects?private_token="+private_token).text)
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
  
                // Build Steps
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
</scriptText>
<usingScriptText>true</usingScriptText>
<sandbox>false</sandbox>
<ignoreExisting>false</ignoreExisting>
<ignoreMissingFiles>false</ignoreMissingFiles>
<failOnMissingPlugin>false</failOnMissingPlugin>
<unstableOnDeprecation>false</unstableOnDeprecation>
<removedJobAction>IGNORE</removedJobAction>
<removedViewAction>IGNORE</removedViewAction>
<removedConfigFilesAction>IGNORE</removedConfigFilesAction>
<lookupStrategy>JENKINS_ROOT</lookupStrategy>
</javaposse.jobdsl.plugin.ExecuteDslScripts>
</builders>
<publishers/>
<buildWrappers/>
</project>

 """

# We get a server object by logging into jenkins with the username and password which we set in initial jenkins setup
# If you had used a different credentials, please the follwowing with valid credentials.
server = jenkins.Jenkins('http://localhost:8080',username='root',password='password')

print("Creating a master job containing DSL script.....")
# Create Job API of python-jenkins will create a job using the xml defined above.
server.create_job('master',job_xml)

print("Building the master job containing DSL script.....")
# Build Job API of Python-Jenkins triggers a build given a valid job name.
server.build_job('master')