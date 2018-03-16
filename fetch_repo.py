"""
    Debojit Kaushik (27th February 2018).
    Script to fetch seleced repositories and push to local
    gitlab server.
"""
import os
import sys
import traceback

def execute_bash(command):
    try:
        return os.system(command)
    except Exception:
        print(traceback.format_exc())

try:
    import requests
except Exception:
    execute_bash("sudo pip3 install requests")
try:
    import gitlab
except Exception:
    execute_bash("sudo pip3 install python-gitlab")


#Variables.
GITHUB_URL = "https://api.github.com/search/repositories?q=language:java"
GITLAB_URL = "http://localhost:80/"
    




def fetch_repos(username, password, gl):
    try:
        #Fetch urls from GitHub API REST.
        r = requests.get(GITHUB_URL, auth = (username,password))
        clone_urls = {}
        
        for item in r.json()['items'][:8]:
            clone_urls[item['name']] = item['clone_url']

        for item in clone_urls:
            execute_bash("git clone " + clone_urls[item])

        for item in clone_urls:
            print("Changing directory to ", item)
            os.chdir(item)
            repo = gl.projects.create({"name":item,"visibility":"public"})
            repo.save()
            url = repo.attributes['http_url_to_repo'].replace("gitlab.example.com", "localhost")
            execute_bash("git remote add gitlab " + url)
            execute_bash("git add --all")
            execute_bash("git commit -m 'Transferring from Github to Gitlab.'")
            execute_bash("git push gitlab") 
            print("Changing back directory")
            os.chdir("..")

        print("...Completed.")
    except Exception:
        print(traceback.format_exc())    


if __name__ == '__main__':
    try:
        print("Gitlab Token: ", end = "")
        token = input()
        gl = gitlab.Gitlab(GITLAB_URL, private_token = (token if token else "sQfyk9sLcJsUxHQB9q-T"))
        fetch_repos(sys.argv[1], sys.argv[2], gl)
    except Exception:
        print(traceback.format_exc())

