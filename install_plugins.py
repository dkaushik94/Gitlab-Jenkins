import os
import sys
import traceback

def execute_bash(command):
    try:
        return os.system(command)
    except Exception:
        print(traceback.format_exc())


try:
    import jenkins
except Exception:
    execute_bash("sudo pip3 install python-jenkins")

import jenkins
server = jenkins.Jenkins('http://localhost:8080',username='root',password='password')
if server.install_plugin("gradle") == True:
    print(" Gradle plugin installed successfully! Please restart jenkins once all plugins are installed")
if server.install_plugin("jacoco") == True:
    print(" Jacoco plugin installed successfully! Please restart jenkins once all plugins are installed")
if server.install_plugin("gitlab-plugin") == True:
    print(" GitLab plugin installed successfully! Please restart jenkins once all plugins are installed")
if server.install_plugin('job-dsl') == True:
    print(" Job DSL plugin installed successfully! Please restart jenkins once all plugins are installed")
