import os
import jenkins
import time
import re

# Run the script to install plugins
# Note that the install_plugins.py installs 4 plugins mentioned down below:
# Jenkins JaCoCo plugin
# GitLab Plugin
# Gradle Plugin
# Job DSL

os.system('python3 install_plugins.py')
time.sleep(4)

# Restart jenkins once plugins are isntalled
os.system('docker restart jenkins-master')

# Sleep for few seconds to ensure jenkins is restarted and is up and running
time.sleep(20)

# Get the jenkins objecy
server = jenkins.Jenkins('http://localhost:8080',username='root',password='password')

# Get all the existing plugins in jenkins
info = server.get_plugins_info()

jacoco_plugin = "Jenkins JaCoCo plugin"
gitlab_plugin = "GitLab Plugin"
gradle_plugin = "Gradle Plugin"
job_dsl_plugin = "Job DSL"

plugins = [jacoco_plugin,gitlab_plugin,gradle_plugin,job_dsl_plugin]

plugin_list = ""
for plugin in info:
    plugin_list = plugin_list + " " + plugin['longName']

# Search for the plugins we just installed in the list of plugins obtained from jenkins
for plugin in plugins:
    assert re.search(plugin, plugin_list, re.IGNORECASE), "Failure - Plugin: " + plugin + " not installed"

print("Success: All the plugins - " + str(plugins) + " are installed")
        

