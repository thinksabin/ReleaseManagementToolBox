_author_ = 'thinksabin'

import requests
import os
import subprocess
import sys
import configparser
from os import path

"""
Sample Usage:
python build_changes_checker.py SBX git-tag-1 git-tag-2
python build_changes_checker.py SBX branch1 branch2
"""


def write_to_file(base_path, base_patch_name, latest_patch_name, reponame):
    with open(base_path +'/' + commits_filename, 'a') as commits_f:

        git_diff = subprocess.Popen(["git", "diff" ,  base_patch_name, latest_patch_name, "--name-only"], stdout=subprocess.PIPE)
        output = git_diff.communicate('')[0]

        if len(output)!=0:

            cf = subprocess.Popen(["git", "log" , '--pretty=format:"%h; subject:%s; author: %cn"', base_patch_name + ".." + latest_patch_name], stdout=subprocess.PIPE)
            commits_output = cf.communicate()

            commits_f.write("============================================================================="+ "\n")
            commits_f.write("Repo : " + str(reponame) + "\n")
            for commits in commits_output:

                commits_f.write(str(commits))
                commits_f.write("\n")
        else:
            print('Could not find proper output from git diff')


def delete_and_create_file(commits_filename):
    file_header = 'Comparing:   : ' + base_patch_name + ' VS ' + latest_patch_name

    if path.exists(commits_filename):
        os.remove(commits_filename)
        print('Old file ', commits_filename, ' removed')

    with open(commits_filename, 'a+') as commits_f:
        commits_f.write(file_header)
        commits_f.write("\n")


def do_bitbucket_api_call(project_url, repos_to_check):


    api_req = requests.get(project_url, auth=(user, password))
    list_of_repos = api_req.json()["values"]
    base_path = os.getcwd()

    for repo in list_of_repos:
        if repo["slug"] in repos_to_check:
            print(repo["slug"])

            if os.path.exists(repo["slug"]):
                os.chdir(base_path + "/" + repo["slug"])
                p = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
                p.communicate()
                write_to_file(base_path, base_patch_name, latest_patch_name, repo["slug"])
                os.chdir(base_path)
            else:
                clone_url = repo["links"]["clone"]
                final_url = ""
                for urls in clone_url:
                    if urls["name"] == "ssh":
                        final_url = urls["href"]
                p = subprocess.Popen(["git", "clone", final_url ], stdout=subprocess.PIPE)
                p.communicate()
                os.chdir(base_path + "/" + repo["slug"])
                p = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
                p.communicate()

                write_to_file(base_path, base_patch_name, latest_patch_name, repo["slug"])
                os.chdir(base_path)



if __name__ == '__main__':
    if len(sys.argv) == 4:

        project_id = sys.argv[1].strip()
        base_patch_name = sys.argv[2].strip()
        latest_patch_name = sys.argv[3].strip()

        try:
            config = configparser.ConfigParser()
            config.read('config.ini')

            user = config['account']['user']
            password = config['account']['password']

            project_url = config[project_id]["project_url"]
            repos_to_check = config[project_id]["repos_to_check"]
            commits_filename = base_patch_name + '_' + latest_patch_name + '.commits'

            delete_and_create_file(commits_filename)
            do_bitbucket_api_call(project_url, repos_to_check)
        except Exception as e:
            print('Couldnt find config.ini file. ')
    else:
        print('Requires 4 arguments like in example')
        print('Sample Usage: python build_changes_checker.py SBX git-tag-1 git-tag-2')

