

import gitlab
import os

# we use python gitlab to fetch info about repos in gitlab
gl = gitlab.Gitlab('http://localhost:80/',private_token='sc24K_e5avo6QjiF7G7c')
num_existing_projects = len(gl.projects.list())

# Before running the script, for testing purposes, set 3 repos to fetch in fetch_repo script
num_of_proj_to_create = 3
# Run the fetch repo script from here. Set the no of repos in the fetch repo script. Use the same below( we use 3)
os.system('python3 fetch_repo.py sandeepjoshi1910 P@ssw0rd')

# Once the repos have been setup, check if the no of repos available in gitlab reflect the ones we just created
# Get the no of existing projects
num_projects = len(gl.projects.list())
assert (num_projects == 3+num_existing_projects), "Fetch Repo did not create the num of projects specified"
print("Test Passed: Fetch Repo script has created appropriate no of projects")

