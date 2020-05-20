from json import dump, load
from os import path, chdir, makedirs, getcwd
from subprocess import Popen
from sys import argv
from github import Github, GithubException
from requests import exceptions

credentials_dir = getcwd()
credentials_path = getcwd() + '/credentials.json'

class Main(object):
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
            self.dir_def = input('Please insert your default project directory: ')
            print()

            credentials = {
                'usr' : self.usr_name,
                'pwd' : self.usr_pwd,
                'dir_def' : self.dir_def
            }
            self.create_credentials(credentials)
            self.create_dir()

    def create_credentials(self, credentials):
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
        self.initialize_git()

    def initialize_git(self):
        git = Github(self.usr_name, self.usr_pwd).get_user()
        
        try:
            git.create_repo(repo_name)
        except GithubException as err:
            print(err)
            choice = input('\n\n\nIt seems that you have entered wrong username or password. Do you wants to change your username and password in credential.json file? (y/n)')
            if (choice.strip() == 'y'):
                chdir(credentials_dir)
                print(getcwd())
                # cmd = Popen('code {}'.format('credentials.json'))
                # cmd.wait()
                # self.usr_name = self.get_credentials()['usr']
                # self.usr_pwd = self.get_credentials()['pwd']
                # chdir(self.repo_dir)
                # self.initialize_git()
            else:
                exit()
        except exceptions.ConnectionError:
            print("Failed to connect to GitHub. Please make sure you're conneccted to the internet.")
        except exceptions.Timeout as err:
            print(err)
            self.initialize_git()
        
        git_cmds = [
            'git init',
            'git remote add origin git@github.com:{}/{}.git'.format(self.usr_name, self.repo_name),
            'touch README.md',
            'git add .',
            'git commit -m "Initial commit"',
            'git push -u origin master',
            'code .'
        ]

        for git_cmd in git_cmds:
            Popen(git_cmd, shell=True).wait()

if __name__ == '__main__':
    try:
        repo_name = str(argv[1])
        Main(repo_name)
    except IndexError:
        print('Please provide directory name')
        exit()