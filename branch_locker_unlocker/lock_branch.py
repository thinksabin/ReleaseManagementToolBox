_author_ = 'thinksabin'
'''
usage:
python lock_branch.py SBX SBX_branchlock.txt develop

'''

import sys
import json
import subprocess
import configparser
from datetime import datetime

date_time = datetime.now()

projectname = sys.argv[1]
project_info_file = sys.argv[2]
branch_to_lock = sys.argv[3]

branch_info_payload = {
     "id": "18",
    "type": "read-only",
    "matcher": {
        "id": branch_to_lock,
        "displayId": branch_to_lock,
        "type": {
            "id": "PATTERN",
            "name": "Pattern"
        },
        "active": "false"
    }
 }

payload_name = 'payload_'+ projectname +'_'+ str(date_time).replace(' ','-').replace(':','-') + '.json'
with open(payload_name, "w") as write_file:
    json.dump(branch_info_payload, write_file)


# reading the text file to lock  

def read_branch_lock(projectID, project_info_file):
    # supplying the project name as the first argument . Example : SBX

    config.read(project_info_file)
    repos = config.get(projectID, 'repo')

    repo_list = repos.split(",")
    file_name = projectID + '_' + str(date_time).replace(' ', '-').replace(':', '-') + '.unlocker'

    with open(file_name,"w") as new_file:
        new_file.close()

    print(('\x1b[6;30;42m''\nLocked Project Details in this file:  %s''\x1b[0m\n\n') %(file_name))

    branch_list = []
    lock_id_list = []

    for eachrepo in repo_list:
        repo_branch_details = lock_branch(projectID, eachrepo)
        branch_list.append(repo_branch_details[0].strip())
        lock_id_list.append(repo_branch_details[1])

    # Sending stdout to a file

    sys.stdout = open(file_name,'a')
    print(('[%s]' % (projectID)))
    print('repo =', repo_list)


    print('branch = ', branch_list)
    print('id = ', lock_id_list) 


# locking the branch
def lock_branch(projectID, eachrepo):

    command_branch_lock = 'curl -s -H "Content-Type: application/json" -u %s:%s -X POST  ' \
                          '%s/rest/branch-permissions/2.0/projects/%s/repos/%s/' \
                          'restrictions -d @%s' %(username, password, bitbucket_url,projectID, eachrepo, payload_name)

    branch_lock = subprocess.Popen(command_branch_lock,shell=True,stdout=subprocess.PIPE, )
    output_lock_branch = branch_lock.communicate()[0]
    load_json = json.loads(output_lock_branch)
    print(load_json)
    lock_id = load_json['id']

    # Extracting the branch name from the JSON file

    current_branch = load_json['matcher']['displayId']
    current_branch = str(current_branch)

    return current_branch, lock_id

if __name__ == '__main__':
    if len(sys.argv) == 4:
        try:

            config = configparser.ConfigParser()
            config.read('config.ini')

            username = config['account']['user']
            password = config['account']['password']
            bitbucket_url = config['account']['bitbucket_url']

        except Exception as e:
            print('Could not find config.ini file. ')

        read_branch_lock(projectname, project_info_file)

    else:
        print('Requires 4 arguments like in example')
        print('Sample Usage: python lock_branch.py SBX SBX_branchlock.txt develop')




