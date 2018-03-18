# Documentation - Tests

### 1. Fetching repos

`fetch_repo_test.py` runs the fetch_repo.py and checks whether the no of repos set to import from github is indeed pushed to gitlab

### 2. Plugin Installation

`plugin_install_test.py` installs the plugins by running the `install_plugins.py` and fetches all plugins installed in jenkins to see if the plugins installed by the script was indeed installed.

### 3. Jenkins Job creation

`jenkins_job_test.py` runs the create_master_job.py to create jobs for each of the repo present in gitlab. Then checks if no of jobs created are equal to the no of repos present.

### 4. Webhook creation

`webhook_test.py` runs the jenkins_job_fetch.py to add webhooks for each jenkins job associated with the gitlab repo. Now once webhooks are setup, we push a sample text file to one of the repo and then check if there was an increment in the build number for the corresponding jenkins job.