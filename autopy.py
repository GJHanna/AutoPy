from json import dump, load, JSONDecodeError
import argparse
from os import path, chdir, makedirs, getcwd
from subprocess import Popen
from github import Github, GithubException
from requests import exceptions

parser = argparse.ArgumentParser(description='A simple script to automate the creation of a project directory with remote GitHub repository')
parser.add_argument('-pv', '--private', action='store_true', help='make remote repository private')
parser.add_argument('repo', nargs='?', help='New repo to create')
parser.add_argument('-ch', '--change', action='store_true', help='edit credentials.json')
parser.add_argument('-v', '--version', action='store_true', help='autopy.py version')

version = 'AutoPy version 2.0'

credentials_dir = getcwd()
credentials_path = getcwd() + '/credentials.json'

class PrettyPrint(object):
    def purple(self, msg):
        print('\033[95m' + msg + '\033[0m')

    def blue(self, msg):
        print('\033[94m' + msg + '\033[0m')
    
    def green(self, msg):
        print('\033[92m' + msg + '\033[0m')
    
    def warning(self, msg):
        print('\033[93m' + msg + '\033[0m')

    def fail(self, msg):
        print('\033[91m' + msg + '\033[0m')

class AutoPy(object):
    def __init__(self, repo_name, is_private):
        self.is_private = is_private
        self.repo_name = repo_name
        self.pretty_print = PrettyPrint()
        self.main()    

    def main(self):
        if (path.isfile(credentials_path)):
            self.usr_name = self.get_credentials()['usr']
            self.usr_pwd = self.get_credentials()['pwd']
            self.dir_def = self.get_credentials()['dir_def']
            self.create_dir()
        else:
            self.pretty_print.purple('This is first time setup')
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
            dump(credentials, credentials_file, sort_keys=True, indent=4, separators=(',', ': '))

    def get_credentials(self):
        try:
            with open('credentials.json') as credentials_file:
                return load(credentials_file)
        except JSONDecodeError as jerr:
            self.pretty_print.fail(jerr)
            self.pretty_print.fail('Invalid directory format in credential.json. Use the -ch flag to edit your project directory')

    def create_dir(self):
        try:
            chdir(path.expanduser('~/'))
            dir = getcwd() + self.dir_def
            chdir(dir)
            self.repo_dir = dir + '/' + self.repo_name
            Popen('mkdir {}'.format(self.repo_dir), shell=True).wait()
            Popen('cd {}'.format(self.repo_dir), shell=True).wait()
            chdir(self.repo_dir)
            self.pretty_print.green('Successfully created directory...')
            self.create_remote_repo()
        except OSError as err:
            self.pretty_print.fail(err)
            self.pretty_print.fail('Invalid directory path. Use the -ch flag to edit your project directory')

    def create_remote_repo(self):
        git = Github(self.usr_name, self.usr_pwd).get_user()
        
        try:
            git.create_repo(self.repo_name, private=self.is_private)
            self.initialize_git()
        except GithubException as err:
            self.pretty_print.warning(err)
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
            self.pretty_print.fail("Failed to connect to GitHub. Please make sure you're conneccted to the internet.")
        except exceptions.Timeout as err:
            self.pretty_print.fail(err)
            self.pretty_print.warning('Attempting to reconnect...')
            self.create_remote_repo()

    def initialize_git(self):
        if (self.is_private):
            msg = 'private'
        else:
            msg = 'public'

        self.pretty_print.warning("Attempting to create '{}' with a {} remote repo".format(self.repo_name, msg))

        git_cmds = [
            'git init',
            'touch README.md',
            'touch .gitignore',
            'git add .',
            'git commit -m "Initial commit"',
            'git remote add origin https://github.com/{}/{}.git'.format(self.usr_name, self.repo_name),
            'git push -u origin master',
        ]

        for git_cmd in git_cmds:
            Popen(git_cmd, shell=True).wait()
        
        exit(self.pretty_print.green("Successfully created '{}' with a {} remote repo".format(self.repo_name, msg)))

if __name__ == '__main__':
    args = parser.parse_args()
    if (args.version):
        print(version)
        exit()
    if (args.change):
        chdir(credentials_dir)
        Popen('nano {}'.format('credentials.json'), shell=True).wait()
        exit()
    try:
        if (args.repo):
            AutoPy(args.repo, args.private)
        else:
            raise TypeError
    except TypeError:
        print('Provide repo name')