import os
import time

replays_dir = 'C:/Users/y/Documents/StarCraft II/Accounts/107039707/2-S2-1-1137385/Replays/Multiplayer'

files_count_was = len(os.listdir(replays_dir))
while True:
    files_count_is = len(os.listdir(replays_dir))
    if files_count_is > files_count_was:
        print('new file identified')
        files_count_was = files_count_is
    time.sleep(1)

