"""
    Debojit Kaushik (27th February 2018).
    Script to fetch seleced repositories and push to local
    gitlab server.

    ***Make sure you have the dependencies installed.
    os, sys, traceback are system bundles.
    Others if missing will be installed in your system. If you dont want them installed in your root,
    please initialize a container or virtual environment to keep the run clean and removable.
"""
import os
import sys
import traceback


def execute_bash(command):
    try:
        return os.system(command)
    except Exception:
        print(traceback.format_exc())


#Exception handling to make sure the modules are installed. 
# Otherwise it will install system wide. 
try:
    import requests
except Exception:
    execute_bash("sudo pip3 install requests")
try:
    import gitlab
except Exception:
    execute_bash("sudo pip3 install python-gitlab")


#URLs( Local Gitlab, Public Github )
GITHUB_URL = "https://api.github.com/search/repositories?q=language:"
GITLAB_URL = "http://localhost"



def fetch_repos(username, password, gl):
    """
        - Fetch list of cloning Urls.
        - Clone repositories into local machine as a mirror.
        - Create local repositories in Gitlab server.
        - Fetch repo urls of local gitlab.
        - Push cloned repositories to local Gitlab server.
    """
    try:
        #Fetch urls from GitHub API REST.
        r = requests.get(GITHUB_URL, auth = (username,password))
        clone_urls = {}
        
        #Selecting 15 repositories only out of 30 fetch.
        for item in r.json()['items'][:15]:
            clone_urls[item['name']] = item['clone_url']

        #Cloning.
        for item in clone_urls:
            execute_bash("git clone " + clone_urls[item])

        #Create and push into gitlab server.
        for item in clone_urls:
            print('\033[1;35mChangin Directory to: %s\033[1;m' %(item))
            os.chdir(item)      #Going into directory of current repo.
            repo = gl.projects.create({"name":item,"visibility":"public"})
            repo.save()
            url = repo.attributes['http_url_to_repo'].replace("gitlab.example.com", "localhost")
            execute_bash("git remote add gitlab " + url)
            execute_bash("git add --all")
            execute_bash("git commit -m 'Transferring from Github to Gitlab.'")
            execute_bash("git push gitlab") 
            print('\033[1;35mChanging back directory to root..\033[1;m')
            os.chdir("..")      #Changin back to one level up in order to go into next REPO_DIR.

        print('\033[1;35m...Completed mirroring repositories via local machine.\033[1;m')
        sys.exit(0)
    except Exception:
        print(traceback.format_exc())    


if __name__ == '__main__':
    try:
        #Personal Access token for access Gitlab API.
        print("\033[1;32mGitlab Personal Access Token: \033[1;m ", end = '')
        token = input()
        while not token:
            print("\033[1;33mPlease provide Personal Access Token:\033[1;m", end = '')
            token = input()
        print("\033[1;32mLanguage of choice: \033[1;m ", end = '')
        language = input()
        while not language:
            print("\033[1;33mPlease provide language you want to fetch repositories of:\033[1;m", end = '')
            token = input()
        language = language.lower().strip()

        #Language shold be prefereably Java for this excercise in order to build successfully.
        if language.lower().strip() != 'java':
            print("\033[1;36mYour language of choice is not Java. The build system MAY fail to build jobs if gradle is absent in the repository. \nDo you want to continue? (Y/N)\033[1;m", end = '')
            choice = input()
            if choice.lower()[0] == 'y':
                pass
            else:
                sys.exit(0)
        GITHUB_URL = GITHUB_URL+language
        gl = gitlab.Gitlab(GITLAB_URL, private_token = (token if token else "sQfyk9sLcJsUxHQB9q-T"))
        fetch_repos(sys.argv[1], sys.argv[2], gl)
    except Exception:
        print(traceback.format_exc())