import os, time, exifread

def GetPictureTakenDate(p_Name):
    f = open(p_Name, 'rb')
    tags = exifread.process_file(f)
    dateTaken = tags['EXIF DateTimeOriginal'].printable
    dateTaken = dateTaken.replace(':', '')
    return dateTaken

files = os.listdir(os.getcwd())
for file in files:
    if os.path.splitext(file)[1].lower() == '.jpg':
        try:
            try:
                dateTaken = GetPictureTakenDate(file)
            except Exception, e:
                print 'Unable to retrieve date on: %s, using modification date'%file
                dateTaken = time.strftime("%Y%m%d", time.localtime(os.path.getmtime(file)))

            # Touch the file and set its modified date
            command = 'touch /D%s/%s/%s /T%s:%s:%s "%s"'%(dateTaken[:4], dateTaken[4:6], dateTaken[6:8], dateTaken[9:11], dateTaken[11:13], dateTaken[13:15], file)
            print command
            os.system(command)

        except Exception, e:
            print 'Unable to retrieve date on: %s'%file
            print e

