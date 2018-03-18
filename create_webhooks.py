"""
    Debojit Kaushik (March 16th, 2018)
    Sandeep Joshi (March 14th 2018)
    Script to fetch job URLs, and create correspoding webhooks to 
    respective repositories.
"""

import jenkins
import sys
import traceback
try:
    import gitlab
except Exception:
    os.system("sudo pip install python-gitlab")
    import gitlab
try:
    import requests
except Exception:
    os.system("sudo pip install requests")
    import requests

GITLAB_URL = "http://localhost:80"
# Logging into jenkins and accessing the server object
server = jenkins.Jenkins('http://localhost:8080', username=sys.argv[1], password=sys.argv[2])

# get jobs API gives us all the jobs with all necessary info about each of them
jenkins_jobs = server.get_jobs()
gl = gitlab.Gitlab(GITLAB_URL, private_token = "8AspReuy7QzCuxRL2jar")

# We need to get URLs of all the jobs so we can use them to add webhooks to each of the repos in gitlab
jenkins_job_urls = {}
for job in jenkins_jobs:
    jenkins_job_urls[job['name']] = job['url'].replace("job", "project").replace("localhost", "172.17.0.3")

repos = gl.projects.list()
for item in jenkins_job_urls:
    try:
        id = 0
        project = 0
        for it in repos:
            #Selecting repository, 
            if it.name.lower() == item.lower():
                if it.name.lower() == 'master':
                    continue
                else:
                    id = it.id
                    project = it
        print("\033[1:32mCreating hook for:\033[1;m", project.name)
        # Creating Hook for current repo.
        try:
            hook = project.hooks.create({
                'url': jenkins_job_urls[item],
                'push_events': 1
            })
            hook.save()     #Saving Hook for the repo.
        except Exception:
            print(traceback.format_exc())
    except Exception as e:
        print(traceback.format_exc())