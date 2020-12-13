# File: depickle.py
# Description: depickles many large objects including maps and graphs
import pickle # for depickling

with open("Pickles/usergraph.pkl", "rb") as input:
    UserGraph = pickle.load(input)
with open("Pickles/idtosongmap.pkl", "rb") as input:
    idToSongMap = pickle.load(input)
with open("Pickles/songtoidmap.pkl", "rb") as input:
    songToIdMap = pickle.load(input)
with open("Pickles/songtotrackmap.pkl", "rb") as input:
    songToTrackMap = pickle.load(input)
with open("Pickles/songtoartistmap.pkl", "rb") as input:
    songToArtistMap = pickle.load(input)
with open("Pickles/songset.pkl", "rb") as input:
    songSet = pickle.load(input)
with open("Pickles/artisttosongmap.pkl", "rb") as input:
    artistToSongMap = pickle.load(input)
