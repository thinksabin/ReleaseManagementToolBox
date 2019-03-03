# ReleaseManagementToolBox
Collection of scripts to help to review build artifacts through git. Can be integrated into CI like Jenkins.
Useful for the DevOps, Development Team, QA, Release Engineer, etc.

Usage for Build changes checker
python build_changes_checker.py SBX git-tag-1 git-tag-2
python build_changes_checker.py SBX branch1 branch2

--------------------
Sample config.ini

[account]
user = myusername
password = mypasswd

[SBX]
project_url = http://bitbucket.mycompany.com:7990/rest/api/1.0/projects/SBX/repos?limit=50
repos_to_check = ["helloworld"]

--------------------

You can add project id as new Sections eg; SBX 
API tested on: Bitbucket
Python 3.7
