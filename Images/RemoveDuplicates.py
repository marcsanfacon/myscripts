#!/usr/local/bin/python3
import os, time, stat, argparse

parser = argparse.ArgumentParser()
args = parser.parse_args()

cur_dir = os.getcwd()
destination_dir = os.path.join(cur_dir, "Duplicates")
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

filesinfo = []
for file in os.listdir(cur_dir):
    name = file[:file.find(' -')]
    stat = os.stat(file)
    filesinfo.append((name, stat.st_mtime, stat.st_size, file))

for filea in filesinfo:
    for fileb in filesinfo:
        if (filea == fileb):
            continue
        elif filea[2] == fileb[2]:
            print('Found potential duplicate, comparing: ', filea[3], fileb[3])
            result =  os.system('cmp -s "' + filea[3] + '" "' + fileb[3] +'"')
            if result == 0:
                print('Confirmed duplicates:', filea[3], fileb[3])
                os.rename(fileb[3], os.path.join(destination_dir, fileb[3]))
