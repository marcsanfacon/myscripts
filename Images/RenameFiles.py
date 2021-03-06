#!/usr/local/bin/python3
import os, time, stat, json, subprocess, argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--prefix", help="Prefix to be added to the renamed file.", default="")
parser.add_argument("--nosuffix", help="No preparation for suffix.", action='store_true', default=False)
args = parser.parse_args()

cur_dir = os.getcwd()
extensions = [ "jpg", "jpeg", "png", "mov", "mp4", "m4v", "heic" ]
destination_dir = os.path.join(cur_dir, "Renamed")
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

command = ["exiftool", "-json", "PrepareFileNames.py"]
files = os.listdir(cur_dir)
command += [file for file in files if not os.path.isdir(os.path.join(cur_dir, file)) ]
p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
lines, error = p.communicate()

for obj in json.loads(lines):
    try:
        if "FileTypeExtension" in obj and obj["FileTypeExtension"].lower() in extensions:
            if "CreateDate" in obj:
                modify_date = obj["CreateDate"]
            else:
                modify_date = obj["FileModifyDate"]
                        
            modify_date = modify_date[:modify_date.find("-")]
            file_time = datetime.strptime(modify_date, "%Y:%m:%d %H:%M:%S")
            src_file = os.path.join(cur_dir, obj["SourceFile"])
            dst_name = file_time.strftime("%Y%m%d %H%M%S")
            if args.prefix != "":
                dst_name += " - " + args.prefix

            if not args.nosuffix:            
                dst_name += " - "
            dst_name += "." + obj["FileTypeExtension"]

            dst_file = os.path.join(destination_dir, dst_name)

            id = 0
            while os.path.exists(dst_file):
                dst_file = os.path.join(destination_dir, dst_name.replace(" - .", "_{} - .".format(id)))
                id += 1

            print('Renaming {} to {}'.format(src_file, dst_file))
            os.rename(src_file, dst_file)

            st = os.stat(dst_file)
            atime = st[stat.ST_ATIME]
            os.utime(dst_file, (atime, file_time.timestamp()))
    except Exception as e:
        print(e)
        
