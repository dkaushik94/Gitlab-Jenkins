import os

print("\033[1;32m Enter the path to the folder containing understand tool: \033[1;m", end = '')
und_path = input()

print("\033[1;32m Enter the path to the repo to be analyzed: \033[1;m", end = '')
repo_path = input()

print("\033[1;32m Enter the path for the results: \033[1;m", end = '')
results_path = input()

print("\033[1;32m Enter the name of project: \033[1;m", end = '')
proj_name = input()

# Create a new understand project
os.system(und_path + "./und create -db " +results_path + proj_name+".udb " + "-languages java" )

# Add the project to be analyzed to the understand project
os.system(und_path + "./und add -db " +results_path + proj_name+".udb " + repo_path)

# Setup the settings for understand project

# Add metrics
os.system(und_path + "./und metrics " + results_path + proj_name+".udb " )

os.system(und_path + "./und settings -metrics all " + results_path + proj_name+".udb " )

os.system(und_path + "./und settings -metricsOutputFile " + results_path+"/metrics.csv " + results_path + proj_name+".udb ")

# Analyze, generate and report metrics
os.system(und_path + "./und analyze " + results_path + proj_name+".udb ")

os.system(und_path + "./und report " + results_path + proj_name+".udb ")

os.system(und_path + "./und metrics " + results_path + proj_name+".udb ")
