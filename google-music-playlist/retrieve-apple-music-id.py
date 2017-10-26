import csv, struct, urllib.parse, urllib.request, json, time, os
from difflib import SequenceMatcher

DEBUG = 0  # Set to 1 for closer inspection

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def retrieve_itunes_identifier(title, artist):
    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0 t:music2",
        "X-Apple-Tz" : "7200" 
    }
    
    search_string = str(artist) +" " + str(title)
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=MusicPlayer&term=" + urllib.parse.quote(search_string)
    request = urllib.request.Request(url, None, headers)

    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        songs = [result for result in data["storePlatformData"]["lockup"]["results"].values() if result["kind"] == "song"]
        
        
        # Attempt to match by title & artist
        for song in songs:
            
            song_match = similar(song["name"].lower() , title.lower())
            artist_match = similar(song["artistName"].lower() , artist.lower())
            
            if DEBUG == 1:
                
                print ("Requested:",artist, " : ",title," => Received:",song["artistName"]," : " ,song["name"])
                print ("Confidence : Artist " + str(round(artist_match*100)),"%  Song " + str(round(song_match*100)) + "%")
                input("Press Enter to continue...")            
            
            
            # For primary matches, lets assume that artist string should always match
            if song["artistName"].lower() == artist.lower():
                if (song["name"].lower() in title.lower()):               
                    return (song["id"],'Primary')
            
                # Attempt to match by title if we didn't get an exact title & artist match
                # For secondary matches, lets assume that artist string should always match
                # return if song title similarty > 80%
             
            elif song["artistName"].lower() == artist.lower():
                if song_match > 0.7:
                    return (song["id"],'Secondary')
                       
            elif artist_match > 0.8:
                if song_match > 0.7:
                    return (song["id"],'Fuzzy')
                
            else:
                print("FAIL: Could not find suitable match for: {} - {}".format(artist, title))
                return None

    except KeyError as e:
        print("FAIL: Nothing returned for: {} - {}".format(artist, title))
        #We don't do any fancy error handling.. Just return None if something went wrong
        return None

for file in os.listdir('playlists'):
    if not os.path.isdir(file) and os.path.splitext(file)[1] == '.csv':
        file = os.path.join('playlists', file)
        print(file)
        itunes_identifiers = []
        not_found = []

        try:
            with open(file, encoding='utf-16-le') as playlist_file:
                playlist_reader = csv.reader(playlist_file, delimiter='\t')
                next(playlist_reader)

                for row in playlist_reader:
                    title, artist, composer, album = row
                    itunes_identifier = retrieve_itunes_identifier(title, artist)

                    if itunes_identifier:
                        if itunes_identifier[1] == 'Primary':
                            itunes_identifiers.append((itunes_identifier, title, artist, album))
                            print("SUCCESS: Exact match: {} - {} => {}".format(title, artist, itunes_identifier[0]))
                        
                        elif itunes_identifier[1] == 'Secondary':
                            itunes_identifiers.append((itunes_identifier, title, artist, album))
                            print("SUCCESS: Secondary match: {} - {} => {}".format(title, artist, itunes_identifier[0]))
                            
                        elif itunes_identifier[1] == 'Fuzzy':
                            itunes_identifiers.append((itunes_identifier, title, artist, album))
                            print("SUCCESS: Fuzzy match: {} - {} => {}".format(title, artist, itunes_identifier[0]))
                    else:
                        not_found.append((title, artist, album))
                        print("{} - {} => Not Found".format(title, artist))


            with open('{} - ID.csv'.format(os.path.splitext(file)[0]), 'w', encoding='utf-8') as output_file:
                for info in itunes_identifiers:
                    output_file.write("{}\t{}\t{}\t{}\n".format(str(info[0][0]), info[1], info[2], info[3]))

            with open('{} - NOT FOUND.csv'.format(os.path.splitext(file)[0]), 'w', encoding='utf-8') as output_file:
                for missing in not_found:
                    output_file.write(str(missing) + "\n")
        except Exception as e:
            print (str(e))
