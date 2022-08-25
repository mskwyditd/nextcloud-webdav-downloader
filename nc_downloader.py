#!/usr/bin/python3
from webdav3.client import Client
import argparse
import getpass
from unidecode import unidecode
import os
from tqdm import tqdm


def get_args() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--login", dest="webdav_login", type=str)

    parser.add_argument("-p", "--password", dest="webdav_password", type=str)
    
    parser.add_argument("-d" ,"--dst-path", dest="dest_path", type=str)

    parser.add_argument("-s", "--src-path", dest="source_path", type=str, default="/")

    return parser.parse_args()

def show_list(client, folder):
    for e, elem in enumerate(client.list(folder)):
        print(elem)

def log_in():
    if not args.webdav_login:
        try:
            user = input("Username: ")
            if user == "":
                login = getpass.getuser()
                args.webdav_login = unidecode(login.lower().replace(" ", "."))
            else:
                args.webdav_login = user
        except Exception as error:
            print('ERROR: error processing login', error)
            exit()

    if not args.webdav_password:
        try:
            args.webdav_password = getpass.getpass()
        except Exception as error:
            print('ERROR: error processing password', error)
            exit()

    if not args.webdav_password:
        print("ERROR: no password was given")
        exit()

    if not args.dest_path:
        args.dest_path = os.getcwd()
    
    if args.dest_path == os.getcwd():
        tmp_path = os.getcwd()
        separ = ("\\" if os.name == 'nt' else "/")
        args.dest_path = tmp_path + separ
        
    tmp_folder = 'nc_downloaded_files'
    iterat = ''
    while os.path.exists(str(args.dest_path) + str(tmp_folder) + str(iterat)):
        if iterat == '': iterat = 0
        iterat += 1
    tmp_folder += str(iterat)

    args.dest_path = str(args.dest_path) + tmp_folder
    
    options = {
    'webdav_hostname': f"https://nc.e-science.pl/remote.php/dav/files/{args.webdav_login}/",
    'webdav_login':    args.webdav_login,
    'webdav_password': args.webdav_password
    }

    client = Client(options)

    return client

class DownloadProgressBar(tqdm):
    def update_to(self, currentsize=0, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(currentsize - self.n)


if __name__ == "__main__":
    args = get_args()
    
    client = log_in()

    try:
        client.free()
    except Exception as e:
        print("ERROR: Username or password was incorrect")
        exit()
    
    if args.source_path == '/':
        show_list(client, "/")
        args.source_path = input("What should be downloaded? (/ or name of folder/file): ")
    
    if not client.check(args.source_path):
        print("ERROR: Folder or file does not exist")
        exit()
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1) as progress_bar:
        client.download_sync(remote_path=args.source_path, local_path=args.dest_path, progress=progress_bar.update_to)
