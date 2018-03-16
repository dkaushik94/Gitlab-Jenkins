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

We now need to setup plugins in jenkins. Run the install_plugins script - `python3 install_plugins.py`<br/>
If the output is `True`, run the command `docker restart jenkins-master` to restart jenkins

![plugin_install](./screenshots/plugin_install.png)

> For some reason, Gitlab plugin is not getting installed through python-jenkins. For this one, we'll install manually.

Go to `Manage Jenkins` > `Manage Plugins`. Click on `Available` tab and search for `Gitlab`. Select and install the plugin.

![gitlab_plugin](./screenshots/gitlab_plugin.png)

### Now we need to configure the gitlab plugin.

Go to `Manage Jenkins` > `Configure System`. Here gitlab section is not configured and should look like this one below

![gitlab_config](./screenshots/gitlab_config.png)

We need to give some details:<br/>
• Connection name : A name for gitlab connection which we'll later refer in each of the job created as well as job DSL. This connection is global for jenkins. We'll give ```gitlab``` as the name.

• Gitlab host url: This is the url of the gitlab container running in the system. We enter `http://172.17.0.2:80/`

• Credentials : We don't have any gitlab credentials setup as of now. We'll create a new one as below. Click on the `Add` button to setup a new credential. Enter the gitlab personal access token generated before. Jenkins will use this credential for various purposes like fetching the repos for jobs</br>

![jenkins_api_credential](./screenshots/jenkins_api_credential.png)

Once this is setup, click on test connection. This should return `success` as shown below.

![gitlab_con_success](./screenshots/gitlab_con_success.png)

> If you are getting any error, check the url of gitlab. It should not be localhost. Since we are running gitlab and jenkins through docker, jenkins and gitlab are running in the lan of docker. jenkins needs to refer to gitlab within that network. So, to get the address of gitlab, in bash of gitlab, find the url at `/etc/hosts` file. Enter that url here.



