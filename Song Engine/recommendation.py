# File: recommendation.py
# Description: implements song recommendation methods

from userclasses import * # for the different user classes
from itemfiltering import * # for content based recommendation methods
from depickle import * # to retrieve the large necessary objects

#constants
GENERIC_USER_ID = "Generic_User_Id"
NUMBER_OF_ORDERS_TO_CONSIDER = 3
SONGS_FROM_EACH_USER = 5
CUTOFF_SIZE = 200
NUMBER_OF_RECOMMENDATIONS = 20
UNSIMILARITY_PENALTY = 50

def getKey(item):
    '''
    Function: getKey
    Behavior: returns second part of item(presumably a tuple)
    Note: used for they key parameter in sorting
    '''
    return item[1]

def sortSongs(songMap):
    '''
    Function: sortSongs
    Parameter: songMap-map from songs to their playcounts
    Behavior: sorts the key-value pairs in a songmap in descending order
    and returns it
    '''
    songTuples = []
    for songId in songMap:
        songTuples.append((songId, songMap[songId]))
    return sorted(songTuples, key = getKey, reverse = True)
   
def genNthOrderConnections(n, currentUserNum):
    '''
    Function: genNthOrderConnections
    Parameter: currentUserNum-number of user to get connections fro
    Behavior: recursively finds the users that are n-orders away from
    a given user in the graph, includes the weight of the users as well
    determined by the sum of 1/connection strengths so that the users
    can be ranked
    '''
    nthOrderConnections = []
    if (n == 0): # base case, corresponds to just the user itself
        nthOrderConnections.append((currentUserNum, 0))
        previouslySeen = {currentUserNum}
        return [nthOrderConnections, previouslySeen]
    oneLower = genNthOrderConnections(n - 1, currentUserNum)
    oneLowerConnections = oneLower[0]
    previouslySeen = oneLower[1]
    for oneLowerConnection in oneLowerConnections: # examines every connection of the n-1st order connections
        userNum = oneLowerConnection[0]
        currentWeight = oneLowerConnection[1]
        connectionWeights = UserGraph.userConnections(userNum)
        for userNum in connectionWeights.getMap():
            if userNum not in previouslySeen:
                previouslySeen.add(userNum)
                # weighting parameter of 1/weight codifies the idea that one of my best friend's best friend
                # is likely more similar to me than my acquaintances
                nthOrderConnections.append((userNum, currentWeight + (1 / connectionWeights.getWeight(userNum))))
    if n == 1: # to not include the user themselves in the list
        oneLowerConnections = []
    return [oneLowerConnections + nthOrderConnections, previouslySeen]

def getRecommendations(songs, iteration):
    '''
    Function: getRecommendations
    Parameters: songs-the songs that the user likes
    iteration-the current state of the program-used to create a new user id
    Behavior: gets 20 recommendation of songs from the input songs
    using collaborative filtering and content based methods
    '''
    candidateSongRecs = userFilteringRecommendations(songs, iteration)
    return applyItemFiltering(candidateSongRecs, songs)

def userFilteringRecommendations(songs, iteration):
    '''
    Function: userFilteringRecommendations
    Parameters: songs-the songs that the user likes
    iteration-the current iteration of the program
    Behavior: generates around 200 candidate songs that the
    user may like using user-baded collaborative filtering
    '''
    UserGraph.addUser(GENERIC_USER_ID + str(iteration))
    for songName in songs:
        songId = songToIdMap[songName]
        UserGraph.addSongToUser(UserGraph.size, songId)
        for userNum in UserGraph.songsToUsers[songId]:
            UserGraph.updateConnections(UserGraph.size, userNum, songId)
    similarUsers = genNthOrderConnections(NUMBER_OF_ORDERS_TO_CONSIDER, UserGraph.size)[0]
    sortedUsers = sorted(similarUsers, key = getKey)
    songRecs = []
    for i in range(len(sortedUsers)):
        user = sortedUsers[i]
        userNum = user[0]
        potentialRecs = sortSongs(UserGraph.getUser(userNum).getTopSongs(SONGS_FROM_EACH_USER))
        for rec in potentialRecs:
            rec = rec[0]
            songRec = idToSongMap[rec]
            if songRec not in songs and songRec not in songRecs:
                songRecs.append(songRec)
        if len(songRecs) > CUTOFF_SIZE:
            break 
    return songRecs

def applyItemFiltering(candidateRecs, songs):
    '''
    Function: applyItemFiltering
    Parameters: candidateRecs-the candidate recommendations generated before
    songs-the songs that the user inputted having liking
    Behavior: uses content based recommendation to downselect
    from the candidate recommendations to the final 20-with a penalty
    for being further down in the candidate list
    '''
    songList = []
    for i in range(len(candidateRecs)):
        song = candidateRecs[i]
        total = 0
        for initSong in songs:
            total += getSimilarityScore(songToTrackMap[song], songToTrackMap[initSong])
        songList.append((song, total - i / UNSIMILARITY_PENALTY))
    contentBasedRecs = []
    numRecs = min(NUMBER_OF_RECOMMENDATIONS, len(songList))
    for song in sorted(songList, key = getKey, reverse = True)[0:numRecs]:
        contentBasedRecs.append(song[0])
    return contentBasedRecs
    
