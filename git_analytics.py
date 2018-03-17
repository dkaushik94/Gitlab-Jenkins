"""
Debojit Kaushik (March 16th 2018)
Script to check the commit history and check
which file has maximum commit and suggest test on the most changed
file of the repository.
"""

import sys, os, traceback
try:
    import git
except Exception:
    print("Missing Dependency! Installing system-wide.")
    os.system("sudo pip3 install gitpython")
    import git
try:
    import requests
except Exception:
    print("Missing Dependency! Installing system-wide.")
    os.system("sudo pip3 install requests")
    import requests


GITHUB_REPOS = 'https://api.github.com/search/repositories?q=language:'
GITHUB_COMMIT_LIST = 'https://api.github.com/repos/'


def calc_changes(repo_sha, gc, output_file, username, password):
    """
        Calculate the most changed file for a commit for a repository.
    """
    try:
        #Iterate over the sha.
        for it, item in enumerate(repo_sha):
            print("\nRepository:","\033[1;35m" ,item, "\033[1;m")
            output_file.write('\n')
            output_file.write("## "+item)
            for item2 in repo_sha[item]:
                #API call to fetch commit meta data like author and files..etc.
                r2 = requests.get(gc + '/' + item2, auth = (username, password))
                changes = 0
                change_file = ''
                #select the most changed file.
                for item3 in r2.json()['files']:
                    if item3['changes'] > changes:
                        change_file = item3['filename']
                        changes = item3['changes']
                    else:
                        pass
                print("For commit","\033[1;32m" ,item2, "\033[1;m",'most changed file is:' , "\033[1;32m", change_file, "\033[1;m")
                out = 'For commit ' + item2 + ' most changed file is: ' + '*' + change_file + '*'
                output_file.write('\n')
                output_file.write("* "+out)

            output_file.write('\n')
                
    except Exception:
        print(traceback.format_exc())


def analytics(username, password):
    """
        Entry function to fetch the repo data for a language and select the required fields.
        And call analytics function on this data.
    """
    try:
        try:
            output_file = open('analytics.md', 'w')
            output_file.write('')
            output_file.write('# GIT ANALYTICS')
        except Exception:
            os.system('touch analytics.txt')
            output_file = open('analytics.txt', 'w')
        
        print("\033[1;37mFetching repository data for 15 repos...\033[1;m", end = '')
        r1 = requests.get(GITHUB_REPOS, auth = (username, password))
        #Running for 15 repositories for this excerise.
        for item in r1.json()['items'][:15]:
            #Construct correct URL to fetch data of the commits of a repo.
            owner = item['owner']['login']
            repo = item['name']
            gc = GITHUB_COMMIT_LIST
            gc = gc + owner + '/' + repo + '/' + 'commits'
            r2 = requests.get(gc, auth = (username, password))
            repo_sha = {}           #Dictionary = {"Name of repo": [sha1, sha2, sha3, sha4]}
            #Construct the repo_sha.
            for item2 in r2.json()[:4]:
                if repo in repo_sha:
                    repo_sha[repo].append(item2['sha'])
                else:
                    repo_sha[repo] = [item2['sha']]
            #Calculate the analytics.
            calc_changes(repo_sha, gc, output_file, username, password)
        output_file.close()
    except Exception:
        print(traceback.format_exc())


#Initiate routine.
if __name__ == "__main__":
    try:
        print("\033[1;37m\nInput language as same as the one with which you fetched repos: \033[1;m", end = '')
        language = input()
        while not language:
            print("Input Language: ", end = '')
            language = input()
        GITHUB_REPOS = GITHUB_REPOS + language
        print("\033[1;32m\nThis script will take the latest 4 commits of the repo and indicate the most\n\
changed file in order to effectively test it and see if there is a patch.\n\033[1;m")
        analytics(sys.argv[1], sys.argv[2])
    except Exception:
        print(traceback.format_exc())