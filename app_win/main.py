import os
import time
import requests

SERVER_URL = 'http://localhost:8000/replay_upload'
REPLAYS_DIR = 'C:/Users/y/Documents/StarCraft II/Accounts/107039707/2-S2-1-1137385/Replays/Multiplayer/'


def replay_upload(replay_path):
    files = {'upload_file': open(replay_path, 'rb')}
    values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
    r = requests.post(SERVER_URL, files=files, data=values)
    print(r)


def main():
    replay_files_was = set(os.listdir(REPLAYS_DIR))
    while True:
        if len(os.listdir(REPLAYS_DIR)) > len(replay_files_was):
            print('new file identified')
            replay_files_is = set(os.listdir(REPLAYS_DIR))
            replay_upload(REPLAYS_DIR + (replay_files_is - replay_files_was).pop())
            replay_files_was = replay_files_is
        time.sleep(1)


if __name__ == '__main__':
    main()
