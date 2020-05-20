from json import dump, load
from os import path, chdir, makedirs, getcwd
from subprocess import Popen
from sys import argv
from github import Github, GithubException
from requests import exceptions

credentials_dir = getcwd()
credentials_path = getcwd() + '/credentials.json'

class AutoPy(object):
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.main()    

    def main(self):
        if (path.isfile(credentials_path)):
            self.usr_name = self.get_credentials()['usr']
            self.usr_pwd = self.get_credentials()['pwd']
            self.dir_def = self.get_credentials()['dir_def']
            self.create_dir()
        else:
            print('\nThis is first time setting.\n')
            self.usr_name = input('Please enter your GitHub user name: ')
            self.usr_pwd = input('Please enter your GitHub password: ')
            self.dir_def = input('Please insert your default project directory /Your/Path: ')
            self.create_credentials()
            self.create_dir()

    def create_credentials(self):
        credentials = {
            'usr' : self.usr_name,
            'pwd' : self.usr_pwd,
            'dir_def' : self.dir_def
            }

        with open('credentials.json', 'w') as credentials_file:
            dump(credentials, credentials_file)

    def get_credentials(self):
        with open('credentials.json') as credentials_file:
            return load(credentials_file)

    def create_dir(self):
        chdir(path.expanduser('~/'))
        dir = getcwd() + self.dir_def
        chdir(dir)
        self.repo_dir = dir + '/' + repo_name
        if (not path.isdir(self.repo_dir)):
            Popen('mkdir {}'.format(self.repo_dir), shell=True).wait()
        Popen('cd {}'.format(self.repo_dir), shell=True).wait()
        chdir(self.repo_dir)
        self.create_remote_repo()
    
    # def check_credentials(self):
    #     print('Your credentials are: \n')
    #     for credentials in self.get_credentials():
    #         print('\t {} : {}'.format(credentials, self.get_credentials()[credentials]))
    #     cred = input('\nEnter 1 to change your username 2 to change your password ')
    #     try: 
    #         cred_num = int(cred)
    #         if (cred_num == 1):
    #             usr_nm = input('Enter your updated username ')
    #             self.usr_name = usr_nm
    #         elif (cred_num == 2):
    #             usr_pwd = input('Enter your updated user password ')
    #             self.usr_pwd = usr_pwd
    #         else:
    #             print('Unkown credential')
    #         self.create_credentials()
    #     except ValueError:
    #         print('Invalid selection. Selection should be an integer')

    def create_remote_repo(self):
        git = Github(self.usr_name, self.usr_pwd).get_user()
        
        try:
            git.create_repo(repo_name)
            self.initialize_git()
        except GithubException as err:
            print(err)
            choice = input('\nIt seems that you have entered wrong username or password. Do you wants to see and change your username and password credentials? (y/n) ')
            if (choice.strip() == 'y'):
                chdir(credentials_dir)
                Popen('nano {}'.format('credentials.json'), shell=True).wait()
                self.usr_name = self.get_credentials()['usr']
                self.usr_pwd = self.get_credentials()['pwd']
                self.create_remote_repo()
            else:
                exit()
        except exceptions.ConnectionError:
            print("Failed to connect to GitHub. Please make sure you're conneccted to the internet.")
        except exceptions.Timeout as err:
            print(err)
            self.create_remote_repo()

    def initialize_git(self):
        git_cmds = [
            'git init',
            'git remote add origin https://github.com/{}/{}.git'.format(self.usr_name, self.repo_name),
            'touch README.md',
            'git add .',
            'git commit -m "Initial commit"',
            'git push -u origin master'
        ]

        for git_cmd in git_cmds:
            Popen(git_cmd, shell=True).wait()

if __name__ == '__main__':
    try:
        repo_name = str(argv[1])
        AutoPy(repo_name)
    except IndexError:
        print('Please provide directory name')
        exit()