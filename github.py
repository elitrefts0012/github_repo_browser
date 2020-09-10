import base64
import getpass
from pprint import pprint
import os

import requests

#pwdinput = getpass.getpass
def search_directory(url):
    print('-'*20)
    resp = requests.get(url, headers=h)
    files = resp.json()
    directories_exist = any([f['type'] == 'dir' for f in files])
    files_exist = any([f['type'] == 'file' for f in files])
    while True:
        if directories_exist:
            print('Directories:')
            for index, repo_file in enumerate(files, 1):
                if repo_file['type'] == 'dir':
                    print(index, repo_file['name'])
        if files_exist and directories_exist: 
            print()
        if files_exist:
            print('Files:')
            for index, repo_file in enumerate(files, 1):
                if repo_file['type'] == 'file':
                    print(index, repo_file['name'])
        selected_file_index = int(input('select file index: '))
        if selected_file_index == -1:
              logout(nickname)
              exit()
        elif selected_file_index == 0:
            return
        else:
            selected_file = files[selected_file_index-1]
            if selected_file['type'] == 'file':
                url = selected_file['url']
                resp = requests.get(url, headers=h)
                print(base64.b64decode(resp.json()['content']).decode('utf-8'))
            else:
                print(url.replace(f'{selected_file["name"]}?ref=master', ''))
                url = selected_file['url']
                search_directory(url)

def save_username_password(username, password, nickname):
    write_file = open(f'saved_username_password/{nickname}', 'a+')
    write_file.write(f'{username}/n{password}')
    write_file.close()

def logout(nickname):
    if os.path.exists(f'saved_username_password/{nickname}'):
        os.remove(f'saved_username_password/{nickname}')
    else:
        print('You are not logged in.')

def login():    
    nickname = input("Enter your nickname, 'create' to save a new account, or 'skip' to not save credentials: ")
    if nickname == 'create':
        nickname = input("Enter new nickname: ")
        username = input("Enter username: ")
        password = getpass.getpass(prompt="Enter password: ")
        save_username_password(username, password, nickname)
    elif nickname == 'skip':    
        username = input("Enter username: ")
        password = getpass.getpass(prompt="Enter password: ")
    elif os.path.exists(f'saved_username_password/{nickname}'):
        read_file = open(f'saved_username_password/{nickname}', 'r')
        username = read_file.readline()
        password = read_file.readline()
        read_file.close()
    else:
        print('That user does not exist, or you misspelled your command.')
        login()
username = ''
password = ''
login()
creds = f"{username}:{password}"
base64creds = base64.b64encode(creds.encode('utf-8')) 
h = {
    "Authorization": f"Basic {base64creds}" 
}
url = f"https://api.github.com/users/{username}/repos"
resp = requests.get(url, headers=h)
repos = resp.json()
while True:
    for index, repo in enumerate(repos, 1):
        print(index, repo['name'])
    print('q quit')
    print('-1 logout')
    print('0 go back')
    selected_repo_index = int(input('select repository index: '))
    if selected_repo_index == -1:
        logout(nickname)
        exit()
    selected_repo = repos[selected_repo_index-1]
    url = selected_repo['contents_url'].replace('{+path}', '')
    search_directory(url)
