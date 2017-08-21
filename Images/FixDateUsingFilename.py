import os, time

files = os.listdir(os.getcwd())
for file in files:
    if os.path.splitext(file)[1].lower() == '.jpg' and os.path.splitext(file)[0].find('19') == 0:
        date = file[:8]

        # Set the dates in the exif
        command = 'exiftool -AllDates="%s/%s/%s 00:00:00" "%s"'%(date[:4], date[4:6], date[6:8], file)
        os.system(command)

        # Touch the file and set its modified date
        command = 'touch /d%s-%s-%s "%s"'%(date[:4], date[4:6], date[6:8], file)
        os.system(command)

