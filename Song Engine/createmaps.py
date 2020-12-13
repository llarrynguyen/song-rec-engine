# File: createmaps.py
# Description: implements methods to create maps relating different Id
# and real-world parameters(ie. map from songId's to songs)
# Note: this code is not meant to be executed again as it could cause
# problems with the pickle file. If its run again, please delete the old pickle
# file to ensure the live program will function properly.

import pickle # for map serialization

def readQuad(line):
    '''
    Function: readQuad
    Parameters: line-line to be read in
    Behavior: reads line into 4 segments
    '''
    index1 = line.find("<SEP>")
    index2 = line.find("<SEP>", index1 + 1)
    index3 = line.find("<SEP>", index2 + 1)
    trackId = line[:18]
    songId = line[23:41]
    artistName = line[46:index3]
    songName = line[index3 + 5:len(line) - 1]
    return [songId, songName, artistName, trackId]
    
def createMaps():
    '''
    Functon: createMaps
    Behavior: reads in track data and creates mappings
    between the different parameters for use in the live program
    and in creating the user graph
    Returns: None
    '''
    idToSongMap = {}
    songToIdMap = {}
    songToArtistMap = {}
    songToTrackMap = {}
    with open("Data/unique_tracks.txt") as infile:
        for line in infile:
            newQuad = readQuad(line)
            idToSongMap[newQuad[0]] = newQuad[1]
            songToIdMap[newQuad[1]] = newQuad[0]
            songToArtistMap[newQuad[1]] = newQuad[2]
            songToTrackMap[newQuad[1]] = newQuad[3]          
    with open("Pickles/idtosongmap.pkl", "wb") as output:
        pickle.dump(idToSongMap, output, pickle.HIGHEST_PROTOCOL)
    with open("Pickles/songtoidmap.pkl", "wb") as output:
        pickle.dump(songToIdMap, output, pickle.HIGHEST_PROTOCOL)
    with open("Pickles/songtoartistmap.pkl", "wb") as output:
        pickle.dump(songToArtistMap, output, pickle.HIGHEST_PROTOCOL)
    with open("Pickles/songtotrackmap.pkl", "wb") as output:
        pickle.dump(songToTrackMap, output, pickle.HIGHEST_PROTOCOL)
         
createMaps()
