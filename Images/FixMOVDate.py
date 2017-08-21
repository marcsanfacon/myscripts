import os, time

files = os.listdir(os.getcwd())
for file in files:
    if os.path.splitext(file)[1].lower() == '.mov' or os.path.splitext(file)[1].lower() == '.mts':
        try:
            dateTaken = time.strftime('%Y%m%d %H%M%S', time.localtime(os.path.getmtime(file)))

            renamed = 0
            cptDay = 1
            while renamed == 0:
                try:
                    newFile = '%s%s'%(dateTaken, os.path.splitext(file)[1].lower())
                    if file <> newFile:
                        print 'Renaming %s -> %s'%(file, newFile)
                        os.rename(file, newFile)
                    renamed = 1
                except:
                    pass
        except Exception, e:
            print 'Unable to retrieve date on: %s'%file
            print e

