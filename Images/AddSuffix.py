import os

for file in os.listdir('.'):
    name, ext = os.path.splitext(file)
    if name.endswith(' - ') and ext in [ '.jpg', '.png', '.mov', '.mp4']:
        name = name.replace(' - ', ' - Scottsdale & Arizona')
        print(name + ext)
        os.rename(file, name+ext)
