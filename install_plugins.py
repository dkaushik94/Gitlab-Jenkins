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

import jenkins

# Get the jenkins server object by logging in to the jenkins. We are using the username and password the same as mentioned in the setup to keep things simple.
# If you set a username and password different from the one mentioned in the documentation, please replace them accordingly.
server = jenkins.Jenkins('http://localhost:8080',username='root',password='password')

# The install plugin API lets us install plugins. It returns True or False based on whether a restart of jenkins is required for the plugin to work. 
# Usually if we try to install a plugin again, it returns False, otherwise it should return True.
# We are installing 4 Plugins: 
# 1) Gradle       2) Jacoco     3) Gitlab       4) Job DSL
if server.install_plugin("gradle") == True:
    print(" Gradle plugin installed successfully! Please restart jenkins once all plugins are installed")
if server.install_plugin("jacoco") == True:
    print(" Jacoco plugin installed successfully! Please restart jenkins once all plugins are installed")
if server.install_plugin("gitlab-plugin") == True:
    print(" GitLab plugin installed successfully! Please restart jenkins once all plugins are installed")
if server.install_plugin('job-dsl') == True:
    print(" Job DSL plugin installed successfully! Please restart jenkins once all plugins are installed")
