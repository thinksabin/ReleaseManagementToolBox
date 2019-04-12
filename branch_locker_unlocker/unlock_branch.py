import sys
import configparser
import subprocess


def UnlockBranch(username, password, unlockerFile):
    print(('unlocker file in use = ', unlockerFile))


    # for selecting the first element before _ in project name file
    config = configparser.ConfigParser()
    config.optionxform = str
    try:
        project = config.read(unlockerFile)
    except Exception as e:
        print('line duplicate: ', e)

    print(("project = ",project))
    project_name = project[0].split('_')[0]

    print(project_name)

    repos = config.get(project_name, 'repo')
    ids = config.get(project_name, 'id')
    repo_list = repos[1:-1].split(", ")
    id_list =  ids[1:-1].split(", ")
    branches = config.get(project_name,'branch')
    branch_list = branches[1:-1].split(", ") 
   
    # appending each repo from repo_list

    repos = []
    for repo in repo_list:
    	repos.append(repo[1:-1])

    # appending each branch from branch_list

    branches = []
    for branch in branch_list: 
        branches.append(branch[1:-1])
                          
    print ('\x1b[6;30;42m''Unlocking the repos''\x1b[0m\n\n')

    # Unlocking the repo from the bitbucket api

    # use of i since repos,id_list and branches all have same number of length
    for i in range(len(repos)):
        print ('\n')
        source_unlock = 'curl -s -X DELETE -u ' \
                        + username + ':' \
                        + password \
                        + ' -H "application/vnd.atl.bitbucket.bulk+json" ' \
                        + bitbucket_url + '/rest/branch-permissions/2.0/projects/' + projectID + '/repos/' \
                        + repos[i] + '/restrictions/' + id_list[i]
        branch_unlock = subprocess.Popen(source_unlock,shell=True,stdout=subprocess.PIPE, ) 
        print('Repo Unlocked : %s ' %(repos[i]))
        print('ID : %s  ' %(id_list[i]))
        print('BRANCH: %s' %(branches[i]))
        


if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:

            config = configparser.ConfigParser()
            config.read('config.ini')

            username = config['account']['user']
            password = config['account']['password']
            bitbucket_url = config['account']['bitbucket_url']
            unlockerFile = sys.argv[1]
            projectID = unlockerFile.split('_')[0]

        except Exception as e:
            print('Couldnt find config.ini file. ')

        UnlockBranch(username, password, unlockerFile)

    else:
        print('Requires 2 arguments like in example')
        print('Sample Usage: python unlock_branch.py projectunlockerfile.unlocker')




