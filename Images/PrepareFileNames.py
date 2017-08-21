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
    #if os.path.splitext(file)[1].lower() == '.jpg' and (os.path.splitext(file)[0].lower().find('img_') == 0 or os.path.splitext(file)[0].lower().find('p1') == 0 or os.path.splitext(file)[0].lower().find('sam_') == 0):
        try:
            try:
                dateTaken = GetPictureTakenDate(file)
            except Exception, e:
                print e
                print 'Unable to retrieve date on: %s, using modification date'%file
                dateTaken = time.strftime("%Y%m%d", time.localtime(os.path.getmtime(file)))

            renamed = 0
            cptDay = 1
            while renamed == 0:
                try:
                    newFile = '%s - .jpg'%(dateTaken)
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

