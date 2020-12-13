# File: textgeneration.py
# Description: implements methods to write to txt and pickle files
# for the purpose of displaying information about the songs
# in the database to the user(both in the program and through searching
# the txt files
# Note: this file is only to be implemented once, if going to re-run, please delete
# all of the old pkl files before doing so. 

import pickle # for object serialization and de-serialization

with open("Pickles/idtosongmap.pkl", "rb") as input:
    idToSongMap = pickle.load(input)

with open("Pickles/songtoartistmap.pkl", "rb") as input:
    songToArtistMap = pickle.load(input)

with open("Pickles/dups.pkl", "rb") as input:
    dups = pickle.load(input)

def generateSongDocs():
    '''
    Function: generateSongDocs
    Behavior: generates documentation and maps
    about the songs and artists in the data
    '''
    songSet = set()
    artistSongs = {}
    with open("Data/train_triplets.txt") as infile:
        for line in infile:
            songName = idToSongMap[line[41:59]]   
            if songName in dups: #song not uniquely identifiable
               continue
            artistName = songToArtistMap[songName]
            songSet.add(songName)
            if artistName not in artistSongs: # need to create set object 
                artistSongs[artistName] = set([])
            artistSongs[artistName].add(songName)
    listOfSongs = open("listofsongs.txt", "w")
    songsByArtist = open("songsbyartist.txt", "w")
    listOfArtists = open("artists.txt", "w")
    alreadyWritten = set()
    for song in songSet: #writes songset to file
        if song not in alreadyWritten:
            alreadyWritten.add(song)
            listOfSongs.write(song + "\n")
    for artist in sorted(artistSongs.keys()): #writes artists and songs by artist file
        listOfArtists.write(artist + "\n")
        songsByArtist.write(artist + "\n")
        for song in sorted(artistSongs[artist]):
            songsByArtist.write(song + "\n")
        songsByArtist.write("\n")
    with open("Pickles/songset.pkl", "wb") as output:
        pickle.dump(songSet, output, pickle.HIGHEST_PROTOCOL)
    with open("Pickles/artisttosongmap.pkl", "wb") as output:
        pickle.dump(artistSongs, output, pickle.HIGHEST_PROTOCOL)
    
generateSongDocs()



