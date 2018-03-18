import os
import jenkins
import time
import random

try:
    print("\033[1;32mEnter path to the repo: \033[1;m", end = '')
    path_to_repo = input()
    
    print("\033[1;32mEnter the name of the project: \033[1;m", end = '')
    project_name = input()

    server = jenkins.Jenkins('http://localhost:8080', username='root', password='password')
    jobs = server.get_all_jobs()

    last_build_number = 0
    try:
        last_build_number = server.get_job_info(project_name)['lastCompletedBuild']['number']
    except expression as identifier:
        print("No builds might have been started yet on this job!\n")

    print("\nNo of builds on this job for the repo as of now: " + str(last_build_number)+"\n")
    
    num = random.randint(1,9999)

    os.system("cd " + path_to_repo + "; touch "+str(num)+".txt ; git add --all ; git commit -m \"test\" ; git push gitlab ")

    print("\nWaiting for few seconds for the build to get triggered...\n")
    time.sleep(40)

    latest_build_number = server.get_job_info(project_name)['lastCompletedBuild']['number']

    print("No of builds on the job after triggering the build: ", "\033[1;34m" +str(latest_build_number) , "\033[1;m")

    assert (latest_build_number > last_build_number), "Failure: Build hasn't been triggered on this job upon a gitlab push"
    print("\033[1;34mSuccess: A build was triggered on this job by a gitlab push. Webhooks are working\033[1;m")

except expression as identifier:
    pass