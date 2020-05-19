from json import dump, load
from os import path, chdir, makedirs, getcwd
from subprocess import Popen
from sys import argv
from github import Github

credentials_path = './credentials.json'
repo_name = str(argv[1])

usr_name = ''
usr_pwd = ''
dir_def = ''

def main():
    global usr_name
    global usr_pwd
    global dir_def

    if (path.isfile(credentials_path)):
        with open('credentials.json') as credentials_file:
            credentials = load(credentials_file)
            usr_name = credentials['usr']
            usr_pwd = credentials['pwd']
            dir_def = credentials['dir_def']
        create_dir()
    else:
        print('\nThis is first time setting.\n')
        usr_name = input('Please enter your GitHub user name: ')
        usr_pwd = input('Please enter your GitHub password: ')
        dir_def = input('Please insert your default project directory: ')
        print()

        credentials = {
            'usr' : usr_name,
            'pwd' : usr_pwd,
            'dir_def' : dir_def
        }

        with open('credentials.json', 'w') as credentials_file:
            dump(credentials, credentials_file)
        create_dir()

def create_dir():
    chdir(path.expanduser('~/'))
    dir = getcwd() + dir_def
    chdir(dir)
    repo_dir = dir + '/' + repo_name
    if (not path.isdir(repo_dir)):
        Popen('mkdir {}'.format(repo_dir), shell=True).wait()
    Popen('cd {}'.format(repo_dir), shell=True).wait()
    chdir(repo_dir)
    initialize_git()

def initialize_git():
    print(getcwd())
    git = Github(usr_name, usr_pwd).get_user()
    git.create_repo(repo_name)
    git_cmds = [
        'git init',
        'git remote add origin git@github.com:{}/{}.git'.format(usr_name, repo_name),
        'touch README.md',
        'git add .',
        'git commit -m "Initial commit"',
        'git push -u origin master',
        'code .'
    ]

    for git_cmd in git_cmds:
        Popen(git_cmd, shell=True).wait()

if __name__ == '__main__':
    main()