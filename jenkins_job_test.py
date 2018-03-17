
import jenkins
import gitlab
import os
import time

# Delete all existing jobs in jenkins
server = jenkins.Jenkins('http://localhost:8080', username='root', password='password')

jobs = server.get_all_jobs()
if(len(jobs) == 0):
    print("No existing jobs.")
else:
    print("Deleting existing jobs: ")
for job in jobs:
    print("Deleting "+job['name'] )
    server.delete_job(job['name'])

# Check for no of available repos in gitlab
print("Checking the no of repos available in Gitlab")
gl = gitlab.Gitlab('http://localhost:80/',private_token='sc24K_e5avo6QjiF7G7c')
num_existing_projects = len(gl.projects.list())
print("num_existing_projects: " + str(num_existing_projects))
print("Gitlab has : " + str(num_existing_projects) + " no of repos")

# Run the script to create jobs in jenkins
os.system('python3 create_master_job.py')

# Wait for few seconds for the master job to build and run DSL to create new jobs
time.sleep(15)
server = jenkins.Jenkins('http://localhost:8080', username='root', password='password')
newly_created_jobs = len(server.get_all_jobs())
print("newly_created_jobs : " + str(newly_created_jobs))
assert (newly_created_jobs == (num_existing_projects + 1))," Failure : A job for each repo in Gitlab has not been created in Jenkins"
print("Success: A job in Jenkins corresponding to each repo in Gitlab has been created")