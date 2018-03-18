# GitLab Setup

## Installing GitLab using the docker image

Run the following command to install gitlab. Once installed, we can see gitlab container running.

```
sudo docker run --detach \
--hostname gitlab.example.com \
--publish 443:443 --publish 80:80 --publish 22:22 \
--name gitlab \
--restart always \
gitlab/gitlab-ce:latest
```

![gitlab_install](./screenshots/gitlab_run.png)

Now go to `https://localhost:80/` to find gitlab up and running. If its not available yet, wait for few minutes till you can see gitlab up and healty. You can find this info by running the command `docker ps -a`

![gitlab_running](./screenshots/gitlab_running.png)

Setup a new password and this will be the password for the user `root` which is by default an admin user. You can create more users as required. Once the password is setup, you can login to gitlab as shown below.

![gitlab_admin_pwd_setup](./screenshots/gitlab_admin_pwd_setup.png)

![gitlab_login](./screenshots/gitlab_login.png)

Now navigate to user's settings. 

![user_settings](./screenshots/user_settings.png)

![user_settings_view](./screenshots/user_settings_view.png)

Navigate to Access Tokens to proceed to generate an access token. Give it a name and expiry date.

![generate_ptoken](./screenshots/generate_ptoken.png)

Once the token is generated, keep it in a secure place. We'll use this token to auto-populate the projects in gitlab server.

![ptoken_done](./screenshots/ptoken_done.png)


We'll now run `fetch_repo.py` to pull projects of a specified language from github and push them to gitlab.

```
python3 fetch_repos.py [github_username] [github_password]
```
Running this command with valid github credentials will then prompt to provide the personal access token which we obtained earlier. Upon entering the token, projects are set up in gitlab.

![repo_fetch](./screenshots/repo_fetch.png)

We can now check gitlab whether all the repos have been set up. We'll setup jenkins now.

![repo_setup_gitlab](./screenshots/repo_setup_gitlab.png)

# Jenkins - Setup

## Install Jenkins

``` zsh
sudo docker pull jenkins
```

``` bash
sudo docker run -p 8080:8080 --name=jenkins-master jenkins
```

Once the jenkins container is running, we need to do a one time setup. As you can see in the terminal, copy the password printed or alternatively the password is always available at : ``` /var/jenkins_home/secrets/initialAdminPassword```

![terminal_jenkins_install](./screenshots/jenkins-installed_new.png)

For this, first login into the container by running the command,

``` sudo docker exec -i -t jenkins-master(name_of_the_image) /bin/bash```

Then navigate to the above path and copy the `initialAdminPassword` to the clipboard

• Now goto `http://localhost:8080/` to find the jenkins up and running as in Fig 1.2
![jenkins_initial_admin_pwd](./screenshots/initial_damin_pwd.png)

Now Paste the `initialAdminPassword` in the clipboard in the jenkins webpage as in Fig 1.3

Click continue. Now jenkins gives options for a custom/suggested installation as in Fig 1.4. We select suggested installation.
![customize_jenkins](./screenshots/customize_jenkins.png)

This will install the standard components as in Fig 1.5

![jenkins_standard_installation](./screenshots/suggested_setup.png)

Once the installation is done, jenkins brings you to create first user. Create an user as shown in Fig 1.6

![jenkins_first_user_creation](./screenshots/first_admin_user_jenkins.png)

Once the user is created, click complete and jenkins in now ready to use! Fig 1.7
![jenkins_user_setup_done](./screenshots/jenkins_ready_to_use.png)

A fresh view of jenkins should look like Fig 1.8

![jenkins_running_done](./screenshots/jenkins_ready.png)

We now need to setup plugins in jenkins. Run the install_plugins script - `python3 install_plugins.py`</br>
If the output is `True`, run the command `docker restart jenkins-master` to restart jenkins

![plugin_install](./screenshots/plugin_install.png)

### Now we need to configure the gitlab plugin.

Go to `Manage Jenkins` > `Configure System`. Here gitlab section is not configured and should look like this one below

![gitlab_config](./screenshots/gitlab_config.png)

We need to give some details:</br>
• Connection name : A name for gitlab connection which we'll later refer in each of the job created as well as job DSL. This connection is global for jenkins. We'll give ```gitlab``` as the name.

• Gitlab host url: This is the url of the gitlab container running in the system. We enter `http://172.17.0.2:80/`

• Credentials : We don't have any gitlab credentials setup as of now. We'll create a new one as below. Click on the `Add` button to setup a new credential. Enter the gitlab personal access token generated before. Jenkins will use this credential for various purposes like fetching the repos for jobs</br>

![jenkins_api_credential](./screenshots/jenkins_api_credential.png)

Once this is setup, click on test connection. This should return `success` as shown below.

![gitlab_con_success](./screenshots/gitlab_con_success.png)

> If you are getting any error, check the url of gitlab. It should not be localhost. Since we are running gitlab and jenkins through docker, jenkins and gitlab are running in the lan of docker. jenkins needs to refer to gitlab within that network. So, to get the address of gitlab, in bash of gitlab, find the url at `/etc/hosts` file. Enter that url here.

## Job Creation

We need to create jobs for each of the repos setup in gitlab. For this we'll use job DSL plugin to do it. Job DSL is written in groovy to fetch all the projects in gitlab and setup a job for each of the repo setup in gitlab. Below is the code for job DSL

> Note: We are using the ip of jenkins and the `private_token` is the Personal Access Token obtained from Gitlab earlier. The token will be different for you. Replace the token in `create_master_job.py` before running the script. If the ip is also different, replace that too.

``` groovy

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
```
We use this code as part of the script in a master job xml. We again use python jenkins to create a master job and then build the created job. This job will inturn create a job for each of the repo in gitlab. It is important to verify the url and replace the `private_token` with the one we got in gitlab.</br>

We need to now run the create_master_job script which will accomplish all of this. Open terminal and run the command `python3 create_master_job.py` </br>

This has now created a job for each of the repo present in the gitlab as shown below

![jobs_created](./screenshots/jobs_created.png)

## Webhooks

Once all the jobs are created in the jenkins, we need to create webhooks. For this we'll run `jenkins_job_fetch.py` which will look at all the jobs created and add webhook to each of the repo in gitlab using python gitlab. Run the command `python3 jenkins_job_fetch.py`. Then head to gitlab to see webhooks created for each project as shown below.</br>

You can naviagate to Integrations part of any of the repo to find the hook created. 

![navigate_to_hook](./screenshots/navigate_to_hook.png)

In the integrations part, once you scroll down, you can see the hook. Click on test and you should see a success message on top. As you can see, the url in the the webhook is the project url of jenkins job.

![hook_created](./screenshots/hook_created.png)

![hook_success](./screenshots/hook_success.png)

Now any push or commits in the repo will automatically trigger a build in jenkins. Lets try that out!</br>

Lets edit the README.md file and push the changes to see if its triggering a build.

![readme_edit](./screenshots/readme_edit.png)

Once the changes are pushed, we head to jenkins job for the same project `MPAndroidChart` and we can see builds have been triggered. On the left bottom corner, we can see builds and a message indicating `Started ​by ​GitLab ​push ​by ​Administrator`

![jenkins_build_trigger](./screenshots/jenkins_build_trigger.png)

# Code Coverage

If the gradlew configuration in build.gradle is correct, builds should work fine and code coverage reports should be generated as below.

![jacoco_0](./screenshots/jacoco_0.png)

![jacoco_1](./screenshots/jacoco_1.png)

![jacoco_2](./screenshots/jacoco_2.png)

# Understand

We use understand to generate the reports for the code analysis. The script `understand.py` uses the understand tool and generates all the results as below.

```
python3 understand.py
```

![class_metrics](./screenshots/class_metrics.png)
![file_metrics](./screenshots/file_metrics.png)
![prog_complex](./screenshots/prog_complex.png)
![proj_metrics](./screenshots/proj_metrics.png)






