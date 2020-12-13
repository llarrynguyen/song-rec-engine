# File: creategraph.py
# Description: houses methods used to create the userGraph and
# serializes the graph
# Retraining Note: when new users are added to the database, their data can be added to the
# MSD data and this code can be used to retrain the whole model. 

from userclasses import * # for the graph, user, and connection classes
import pickle #graph serialization 

TOP_LISTENERS_LENGTH = 5 # number of new connections to form between user and their similar users

        
def readTrip(line):
    '''
    Function: readTrip
    Parameter: line
    Behavior: reads line into it's three constituents
    '''
    userId = line[:40]
    songId = line[41:59]
    playCount = line[60]
    return [userId, songId, playCount]

def createGraph():
    '''
    Function: createGraph
    Behavior: reads triplet data from MSD into graph connecting users
    and dumps graph into pickle file for later retrieval
    '''
    Graph = userGraph()
    with open("Data/train_triplets.txt") as infile:
        for line in infile:
            newTrip = readTrip(line)
            userId = newTrip[0]
            newSongId = newTrip[1]
            playCount = int(newTrip[2])
            Graph.addElement(userId, newSongId, playCount)
        Graph.update(TOP_LISTENERS_LENGTH)
    with open("Pickles/usergraph2.pkl", "wb") as output:
        pickle.dump(Graph, output, pickle.HIGHEST_PROTOCOL)

createGraph()
        


        
                
                
                
    
