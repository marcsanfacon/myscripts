import os, time

files = os.listdir(os.getcwd())
for file in files:
    if os.path.splitext(file)[1].lower() == '.jpg' or os.path.splitext(file)[1].lower() == '.png':
        newFile = file.replace('  ', ' ')
        if newFile != file:
	    print newFile
	    os.rename(file, newFile)
