import os, time, exifread

def GetPictureTakenDate(p_Name):
    f = open(p_Name, 'rb')
    tags = exifread.process_file(f)
    dateTaken = tags['EXIF DateTimeOriginal'].printable
    dateTaken = dateTaken.replace(':', '')
    return dateTaken

files = os.listdir(os.getcwd())
for file in files:
    if os.path.splitext(file)[1].lower() == '.jpg' or os.path.splitext(file)[1].lower() == '.png':
    #if os.path.splitext(file)[1].lower() == '.jpg' and (os.path.splitext(file)[0].lower().find('img_') == 0 or os.path.splitext(file)[0].lower().find('p1') == 0 or os.path.splitext(file)[0].lower().find('sam_') == 0):
        try:
            try:
                dateTaken = GetPictureTakenDate(file)
            except Exception, e:
                print e
                print 'Unable to retrieve date on: %s, using modification date'%file
                dateTaken = time.strftime("%Y%m%d %H%M%S", time.localtime(os.path.getmtime(file)))

            renamed = 0
            cptDay = 1
            while renamed == 0:
                try:
                    # Touch the file and set its modified date
                    command = 'touch /D%s/%s/%s /T%s:%s:%s "%s"'%(dateTaken[:4], dateTaken[4:6], dateTaken[6:8], dateTaken[9:11], dateTaken[11:13], dateTaken[13:15], file)
                    command = 'touch -t %s%s%s%s%s.%s "%s"'%(dateTaken[:4], dateTaken[4:6], dateTaken[6:8], dateTaken[9:11], dateTaken[11:13], dateTaken[13:15], file)
                    print command
                    os.system(command)
                    
                    newFile = '%s - .jpg'%(dateTaken)
                    if file == newFile:
                        break

                    if os.path.exists(newFile):
                        newFile = '%s - %03d.jpg'%(dateTaken, cptDay)
                        cptDay += 1

                    os.rename(file, newFile)
                    print 'Renaming %s -> %s'%(file, newFile)
                    renamed = 1
                except:
                    pass
        except Exception, e:
            print 'Unable to retrieve date on: %s'%file
            print e

