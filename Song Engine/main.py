# File: main.py
# Description: runs program for generating recs based on user input
# intended to be used by a variety of people 
# Note: driver file for entire program
# Second Note: starter code for the frontend was taken from the PySimpleGui cookbook

import PySimpleGUI as sg # for graphics
from recommendation import * # for the recommendation system

INSTRUCTIONS = "Instructions: Please input one song at a time and then click the 'Get Recommendations'\n \
button to get your recommendations. Use first box to get the supported songs for that artist."

def runProgram():
    '''
    Function: runProgram
    Behavior: implements program to get song input from user
    and outputs recommendations for their top songs
    '''
    layout = [[sg.Text('Welcome to The Song Recommendation Engine', font = ('Helvetica', 20), text_color = "black")],
          [sg.Text(INSTRUCTIONS, font = ('Helvetica', 16), text_color = "grey")],
          [sg.Text('Input an artist to get the corresponding songs: ', font = ('Helvetica', 25), text_color = "black")],
          [sg.Input(do_not_clear = False)],
          [sg.Button('Get Songs')],
          [sg.Text('Please enter your favorite songs: ', font = ('Helvetica', 25), text_color = "black")],
          [sg.Input(do_not_clear = False)],
          [sg.Button('Input Song'), sg.Button('Give Recommendations')]]
    window = sg.Window('Song Recommendation Engine', layout)
    songs = set()
    iteration = 1
    while True:  # Event Loop
        event, inputs = window.read()
        if event == "Give Recommendations": # user is ready to receive their recommendation
            if songs == set(): # user has entered no songs
                sg.popup('Error: You have not entered any songs', font = ('Helvetica', 18), text_color = "red")
                continue
            songRecs = getRecommendations(list(songs), iteration)
            if songRecs == []: # recommendations came up early, implying a lack of data
                sg.popup('You have not inputted enough information to give meaningful recommendations.', output, font = ('Helvetica', 18), text_color = "black")
            else:
                output = 'These are the top 20 songs we recommend for you: \n'
                for songRec in songRecs:
                    output += songRec + " by " + songToArtistMap[songRec] + "\n"
                sg.popup(output, font = ('Helvetica', 18), text_color = "black")
            songs = set()
            iteration += 1
        if event is None: # user has entered the program
            break
        if event == "Get Songs": # user wants to get the supported songs from a certain artist 
            artist = inputs[0]
            if artist not in artistToSongMap:
                sg.popup("Error: Database does not contain that artist", font = ('Helvetica', 18), text_color = "red")
            else:
                output = "List of Supported Songs: \n"
                for song in artistToSongMap[artist]:
                    output += song + "\n"
                sg.popup(output, font = ('Helvetica', 18), text_color = "red")
        if event == 'Input Song': #user would like their inputted song to be recoreded
            if inputs[1] not in songSet or inputs[1] == "":
                sg.popup('That is not a valid song name.', font = ('Helvetica', 18), text_color = "red")
            else:    
                songs.add(inputs[1])       
    window.close()

runProgram()




