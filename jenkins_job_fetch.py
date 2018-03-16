import jenkins

server = jenkins.Jenkins('http://localhost:8080',username='sandeep',password='password')
jenkins_jobs = server.get_jobs()
for job in jenkins_jobs:
    print(job['url'])