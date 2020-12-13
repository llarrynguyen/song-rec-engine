# File: userclasses.py
# Description: implements the User, Connection, and userGraph classes
# which are used to store user data and relationship between users

#constants
NULL = "NULL"
MAX_PLAYCOUNT = 100 #implied playcount of a user liking a song

class User(object):
    def __init__(self):
        '''
        Method: __init__
        Behavior: initializes user object with empty song
        and connections component
        '''
        self.songs = {}
        self.connections  = Connections()
    
    def getTopSongs(self, numSongs):
        '''
        Method: getTopSongs
        Parameter: numSongs-number of top songs to retrieve
        Behavior: finds a user's top numSongs number of songs
        and returns the map from these songs to the playcounts
        '''
        minimumMax = MAX_PLAYCOUNT
        minId = NULL
        topSongs = {}
        songs = []
        for song in self.songs:
            if len(topSongs) < numSongs: # haven't added enough yet
                topSongs[song] = self.songs[song]
                if topSongs[song] < minimumMax:
                    minId = song
                    minimumMax = topSongs[song]
            else:
                if self.songs[song] > minimumMax: # song should be added
                    del topSongs[minId]
                    curMinId = 0
                    curMinMax = 100
                    for song in topSongs:
                        if topSongs[song] < curMinMax:
                            curMinId = song
                            curMinMax = topSongs[song]
                    minId = curMinId
                    minimumMax = curMinMax
        return topSongs
    
    def getConnections(self):
        '''
        Method: getConnections
        Behavior: gets a user's connections object and returns it
        '''
        return self.connections
    
    def updateConnections(self, userNumber, weight):
        '''
        Method: updateConnections
        Parameters: userNumber-number of user's new connection
        weight-weight of the new connection
        Behavior: updates a user's connections with a new user
        and the weight of that connection
        '''
        self.connections.updateConnection(userNumber, weight)
        
    def addSong(self, songId, playCount):
        '''
        Method: addSong
        Parameters: songID-id of song to add
        playCount-number of plays of given song
        Behavior: adds song to list of users listened
        to songs with the corresponding playcount
        '''
        self.songs[songId] = playCount
    
    def getPlayCount(self, songId):
        '''
        Method: getPlayCount
        Parameters: songID,
        Behavior: gets the playcount for a given
        song and returns it
        '''
        return self.songs[songId]
    
    def getSongs(self):
        '''
        Method: getSongs
        Behavior: returns a users songMap
        '''
        return self.songs

    def hasListenedTo(self, songId):
        '''
        Method: hasListenedTo
        Parameter: songId-id of song to determine
        Behavior: returns whether a user
        has listened to a given song
        '''
        return (songId in self.songs)
    

class Connections:
    def __init__(self):
        '''
        Method: __init__
        Behavior: initializes a connection
        '''
        self.userWeights = {}
    
    def getMap(self):
        '''
        Method: getMap
        Behavior: returns the map from users to weights for the connections object
        '''
        return self.userWeights
    
    def getWeight(self, userNumber):
        '''
        Method: getWeight
        Parameter: userNumber-number of user to retrieve weight with
        Behavior: returns the weight of connection to a given userNumber
        '''
        return self.userWeights[userNumber]
    
    def containsUser(self, userNumber):
        '''
        Method: containsUser
         Parameter: userNumber-number of user to determine about
        Behavior: returns whether the connection object contains a reference
        to a given user
        '''
        return userNumber in self.userWeights
    
    def updateConnection(self, userNumber, weight):
        '''
        Method: updateConnection
        Parameter: userNumber-userNumber to update
        weight-additional weight to add
        Behavior: updates the connections object with the given user
        with the additional weight, initializing the connection
        if it has not yet been formed
        '''
        if not self.containsUser(userNumber):
            self.userWeights[userNumber] = weight
        else:
            self.userWeights[userNumber] += weight
            

class userGraph(object):
    def __init__(self):
        '''
        Method: __Init__
        Behavior: initializes a user-graph object with everything set empty
        '''
        self.users = {} # map from user's number to users number -> User
        self.userNumbers = {} # map from user ids to number
        self.songsToUsers = {} #map from songs to a set of the user id's of listeners string -> set string
        self.size = 0
    
    def addUser(self, userId):
        '''
        Method: addUser
        Parameter: userId-id of user to add to graph
        Behavior: adds empty user to map
        Note: only used for recommendation, not part of graph building
        '''
        self.size += 1
        self.userNumbers[userId] = self.size
        self.users[self.size] = User()
    
    def addSongToUser(self, userNum, songId):
        '''
        Method: addUser
        Parameter: userNum-userNumber
        songId-Id of song to add
        Behavior: adds a song to user object
        Note: only use for recommendation, not part of graph building
        '''
        self.users[userNum].addSong(songId, MAX_PLAYCOUNT)
    
    def getUser(self, userNum):
        '''
        Method: getUser
        Parameter: userNum-user number to retrieve
        Behavior: returns user object associated with specified number
        '''
        return self.users[userNum]
    
    def userConnections(self, userNum):
        '''
        Method: userConnections
        Parameter: userNum-userNumber to retrieve from
        Behavor: returns a user's connection object
        '''
        return self.users[userNum].getConnections()

    def updateConnections(self, user1Num, user2Num, songId):
        '''
        Method: updateConnections
        Parameter: user1Num-1st user number
        user2Num-2nd user number
        songId-Id of song
        Behavor: uodates the connections between the 2 users in light
        of the given song
        '''
        user1PlayCount = self.users[user1Num].getPlayCount(songId)
        user2PlayCount = self.users[user2Num].getPlayCount(songId)
        additionalWeight = min(user1PlayCount, user2PlayCount)
        self.users[user1Num].updateConnections(user2Num, additionalWeight)
        self.users[user2Num].updateConnections(user1Num, additionalWeight)

    def addElement(self, userId, songId, playCount):
        '''
        Method: addElement
        Parameter: userId-userId of triplit data
        songId-songId from triplet data
        Playcount-playcount from triplet data
        Behavior: updates user to have listened to the given song
        and adds user to the songsMap of the graph
        '''
        if userId not in self.userNumbers:
            self.addUser(userId)
        if songId not in self.songsToUsers:
            self.songsToUsers[songId] = set()
        userNumber = self.userNumbers[userId]
        self.users[userNumber].addSong(songId, playCount)
        self.songsToUsers[songId].add(userNumber)

    def update(self, topListenersLength):
        '''
        Method: update
        Parameter: topListenersLength-number of users to form connections
        between at max for each song
        Behavior: using songMap-iteratively forms and updates connections
        between the different users
        '''
        for songId in self.songsToUsers: # for each song in the map
            topListeners = [] # users who like the song the most
            minimumMax = MAX_PLAYCOUNT
            minIndex = 0
            for userNumber in self.songsToUsers[songId]: # for each user who listened to that song
                length = len(topListeners)
                if length < topListenersLength:
                    topListeners.append(userNumber)
                    count = self.users[userNumber].getPlayCount(songId)
                    if count < minimumMax:
                        minIndex = length
                        minimumMax = count
                else:
                    count = self.users[userNumber].getPlayCount(songId)
                    if count <= minimumMax:
                        continue
                    else:
                        topListeners.append(userNumber)
                        del topListeners[minIndex]
                        minIndex = 4
                        minimumMax = count
                        for number in range(topListenersLength):
                            newCount = self.users[topListeners[number]].getPlayCount(songId)
                            if newCount < minimumMax:
                                minIndex = number
                                minimumMax = newCount                    
            for i in range(len(topListeners)): # for the top listeners of the song
                for j in range(i + 1, len(topListeners)):
                    # form connections between top listeners of the given song
                    self.updateConnections(topListeners[i], topListeners[j], songId) 
            self.songsToUsers[songId] = set(topListeners)
            #updates map to only include top listeners so to dilute the large number of one time-listeners
            # of many songs
        self.userNumbers = {} #this map no longer needed and is large so it is cleared
        # prior to pickling
        
            
 

            



        
    
    
        
    
    
        


    
        
        



    
