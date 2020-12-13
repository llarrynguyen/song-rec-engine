# File: dups.py
# Description: builds the set of songs with multiple ID's
# and exports the object to a pickle file
# Note: this code is not meant to be executed again as it could cause
# problems with the pickle file. If its run again, please delete the old pickle
# file to ensure the live program will function properly.  

import pickle # for set serialization

def readPair(line):
    """
    Function: readPair
    Parameters: line
    Behavior: finds songId and songName in
    the line and returns them
    """
    index1 = line.find("<SEP>")
    index2 = line.find("<SEP>", index1 + 1)
    index3 = line.find("<SEP>", index2 + 1)
    songId = line[23:41]
    songName = line[index3 + 5:len(line) - 1]
    return songId, songName
    
def createDups():
    """
    Function: createDups
    Parameters: None
    Behavior: Generates list of songs with multiple Id's
    corresponding to a song name not being uniquely defined
    and therefore unusable in the program.
    """
    songsToIds = {}
    with open("Data/unique_tracks.txt") as infile:
        for line in infile:
            songId, songName = readPair(line)
            if songName not in songsToIds: # need to add name to the map
                songsToIds[songName] = set()
            songsToIds[songName].add(songId)
    dups = set()
    for key in songsToIds:
        if len(songsToIds[key]) > 1: # songname is not uniquely defined
            dups.add(key)
    with open("Pickles/dups.pkl", "wb") as outfile:
        pickle.dump(dups, outfile, pickle.HIGHEST_PROTOCOL)
        
createDups()

            
