import os
import time
import glob
import requests
from multiprocessing import Queue  # fixes "module queue not found" issue for built app

DEFAULT_SERVER_PATH = 'http://localhost:8765/replay_upload'
CUSTOM_SERVER_PATH_FILENAME = 'SERVER_PATH.txt'
if os.path.exists(CUSTOM_SERVER_PATH_FILENAME):
    with open(CUSTOM_SERVER_PATH_FILENAME, 'r') as file:
        DEFAULT_SERVER_PATH = file.readline()[:-1]
else:
    print(CUSTOM_SERVER_PATH_FILENAME, 'not found at', os.getcwd())


def replay_upload(server_url, replay_path):
    with open(replay_path, 'rb') as file:
        files = {'upload_file': file}
        values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
        r = requests.post(server_url, files=files, data=values)
    print(time.ctime(), ':: replay sending status is', r)


def main():
    server_url = input('Input your server path [' + DEFAULT_SERVER_PATH + ']: ') or DEFAULT_SERVER_PATH
    possible_replays_dir = glob.glob('C:/Users/*/Documents/StarCraft II/Accounts/*/*/Replays/Multiplayer/')
    possible_replays_dir = '' if not len(possible_replays_dir) else possible_replays_dir[0]
    replays_dir = input('Input your replays path [' + possible_replays_dir + ']: ') or possible_replays_dir
    replay_files_was = set(os.listdir(replays_dir))
    print('Tracking replays folder for new ones...')
    while True:
        if len(os.listdir(replays_dir)) > len(replay_files_was):
            print('New replay identified. Trying to send it to server...')
            replay_files_is = set(os.listdir(replays_dir))
            replay_upload(server_url, replays_dir + (replay_files_is - replay_files_was).pop())
            replay_files_was = replay_files_is
        time.sleep(1)


if __name__ == '__main__':
    main()
