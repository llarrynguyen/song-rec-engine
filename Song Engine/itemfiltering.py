# File: contentmethods.py
# Description: implements methods for song ranking based off of their
# content, specifically the tags associated with each song

import sqlite3 # for accessing the million song database tags data

def getTags(tid):
    """
    Function: getTags
    Parameter: tid-the track of a song
    Behavior: returns the tags associated with a song
    Note: code for sql data retrieval adapted from MSD demo
    """
    dbfile = "Data/lastfm_tags.db" #file with tags data
    conn = sqlite3.connect(dbfile)
    sql = "SELECT tags.tag, tid_tag.val FROM tid_tag, tids, tags WHERE tags.ROWID=tid_tag.tag AND tid_tag.tid=tids.ROWID and tids.tid='%s'" % tid
    res = conn.execute(sql)
    tags = res.fetchall()
    tagsNoWeight = set()
    for tag in tags:
        tagsNoWeight.add(tag[0].lower())
    return tagsNoWeight

def getSimilarityScore(tid1, tid2):
    '''
    Function: getSimilarityScore
    Parameters: tid1, tid2-track id's of the two songs 
    Behavior: returns the similarity of two songs
    '''
    tags1 = getTags(tid1)
    tags2 = getTags(tid2)
    # number of same tags
    return len(tags1.intersection(tags2)) 




    
        
