"""
Author: Kevin Peterson
Class: CS361: Software Engineering I
Date: 2/6/22
Description: Hangman Web App core logic
"""

# Imports
from flask import Flask, render_template
from flask import request, redirect
import random
import urllib
import time
import sys


# Create the web application
hangmanApp = Flask(__name__)

#--------------------------------------------------------------------------------------------
# Game Logic
#--------------------------------------------------------------------------------------------

class GameTimer:
    def __init__(self):
        self.timeOfCreation = time.time()

    def getTimeElapsed():
        return time.time() - self.timeOfCreation()

class Game:
    def __init__(self):
        # Game state
        self.round = 0
        self.currentWord = ""
        self.guessesUsed = 0
        self.lettersPerRound = [4, 5, 6, 7, 8]
        self.guessesPerRound = [4, 5, 6, 7, 8]
        self.timeLimitPerRound= [60, 75, 90, 115, 130]
        self.incorrectGuesses = []
        self.currentProgress = []
        self.dictionary = [[],[],[],[],[]]
        self.timer = None
        self.displayError = ""
        self.gameWon = False
        self.gameLost = False
        # used for reporting game state after winning or losing
        self.correctGuesses = []
        self.lastWord = ""

        # Settings
        self.showCorrectLetters = True
        self.showCorrectLettersDefault = True
        self.showContainedLetters = True
        self.showContainedLettersDefault = True
        self.preventInvalidWords = True
        self.preventInvalidWordsDefault = True
        self.preventUsedLetters = True 
        self.preventUsedLettersDefault = True 
        self.useTimeLimit = True
        self.useTimeLimitDefault = True
        self.tutorialMode = False
        self.tutorialModeDefault = False

        # setup our dictionary
        self.buildDictionary()

    # pulls word list from internet and builds dictionary for future use
    def buildDictionary(self):
        url = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"

        file = urllib.request.urlopen(url)

        # parse words from online tab and put them into separate list for 4, 5, 6, 7, and 8 letter words
        for line in file:
            decoded_line = line.decode("utf-8")
            stripped_line = ''.join([i for i in decoded_line if not i.isdigit()]) # strip numbers
            stripped_line = stripped_line.replace(" ", "") # kill spaces
            stripped_line = stripped_line.rstrip("\n") # strip new line chars
            stripped_line = stripped_line.lstrip() # strip leading spaces

            if len(stripped_line) == 4:
                self.dictionary[0].append(stripped_line)
            elif len(stripped_line) == 5:
                self.dictionary[1].append(stripped_line)
            elif len(stripped_line) == 6:
                self.dictionary[2].append(stripped_line)
            elif len(stripped_line) == 7:
                self.dictionary[3].append(stripped_line)
            elif len(stripped_line) == 8:
                self.dictionary[4].append(stripped_line)

    # get a random word of specified length (based on round)
    def getRandomWordForRound(self):
        return random.choice(self.dictionary[self.round]).lower()

    # returns the current word for the round
    def getCurrentWord(self):
        return self.currentWord

    # get user progress on current word
    def getProgress(self):
        return self.currentProgress

    # get current round number (offset by 1 for human readability)
    def getRoundNumber(self):
        return self.round + 1

    # get letters in word this round
    def getLettersInWord(self):
        return self.lettersPerRound[self.round]

    # return number of guesses remaining
    def getGuessesRemaining(self):
        return self.guessesPerRound[self.round] - self.guessesUsed
    
    # return total number of guesses allowed in the current round
    def getGuessesThisRound(self):
        return self.guessesPerRound[self.round]

    # get incorrect guesses so far
    def getIncorrectGuesses(self):
        return self.incorrectGuesses

    # gets the elapsed time for the current round
    def getTimeElapsed(self):
        return self.roundTime

    # get the total time allowed in the given round
    def getTimeAllowedInCurrentRound(self):
        return self.timeLimitPerRound[self.round]

    # gets the total time remaining in the round
    def getTimeRemainingInCurrentRound(self):
        return self.getTimeAllowedInCurrentRound() - self.getTimeElapsed()

    def isGameWon(self):
        return self.gameWon

    def isGameLost(self):
        return self.gameLost

    def resetGameState(self):
        self.round = 0
        self.currentWord = ""
        self.guessesUsed = 0
        self.lettersPerRound = [4, 5, 6, 7, 8]
        self.guessesPerRound = [4, 5, 6, 7, 8]
        self.timeLimitPerRound= [60, 75, 90, 115, 130]
        self.incorrectGuesses = []
        self.currentProgress = []
        self.timer = None
        self.displayError = ""
        self.gameWon = False
        self.gameLost = False

    #----------------------
    # Game events
    #----------------------

    # process user guess attempt (userGuessString all lowercase)
    def processAttempt(self, userGuessString):
        # validate attempt (dont ding user for bad guess)
        if len(userGuessString) < game.getLettersInWord():
            self.displayError = " has too few letters, please try again."
            return userGuessString
        elif len(userGuessString) > game.getLettersInWord():
            self.displayError = " has too many letters, please try again."
            return userGuessString
        elif not userGuessString in self.dictionary[self.round]:
            self.displayError = " was not found in game dictionary, please try again."
            return userGuessString
        elif userGuessString in self.incorrectGuesses:
            self.displayError = " has already been tried, please try again."
            return userGuessString
        else:
            # update current progress for display
            for i in range(len(self.currentWord)):
                if self.currentWord[i] == userGuessString[i]:
                    self.currentProgress[i] = self.currentWord[i]

            # handle correct vs. incorrect guess
            self.displayError = ""
            if userGuessString == self.currentWord.lower():
                self.gameEvent_onCorrectGuess()
            else:
                self.gameEvent_onIncorrectGuess(userGuessString)

            return ""

    # method to start a new game round
    def gameEvent_startNextRound(self):
        self.currentWord = self.getRandomWordForRound()
        self.lastWord = self.currentWord
        self.currentProgress = []
        for i in range(len(self.currentWord)):
            self.currentProgress.append(".")

        self.timer = GameTimer()

    # on correct guess, progress to next round
    def gameEvent_onCorrectGuess(self):
        self.round += 1

        self.correctGuesses.append(self.currentWord)

        if self.round >= len(self.lettersPerRound):
            self.gameEvent_onWinGameComplete()
        else:
            self.guessesUsed = 0
            self.incorrectGuesses = []
            self.guessesThisRound = self.getGuessesThisRound()
            self.gameEvent_startNextRound()

    # on incorrect guess
    def gameEvent_onIncorrectGuess(self, userGuessString):
        self.guessesUsed += 1
        self.incorrectGuesses.append(userGuessString)

        if self.guessesUsed >= self.getGuessesThisRound():
            self.gameEvent_onLose()

    # on win entire game
    def gameEvent_onWinGameComplete(self):
        self.gameWon = True

    # on fail state - game over
    def gameEvent_onLose(self):
        self.gameLost = True


# Create game instance and start first round
game = Game()
game.gameEvent_startNextRound()

#--------------------------------------------------------------------------------------------
# @hangmanApp.route provides a route where requests on the web application can be addressed
#--------------------------------------------------------------------------------------------

# Home page Route
@hangmanApp.route('/', methods = ['POST', 'GET'])
def index():
    game.resetGameState()
    return render_template('_hangman_home.html')

# Start new game
@hangmanApp.route('/play', methods = ['POST', 'GET'])
def startGame():
    # if game just started and no word is chosen, grab a random one
    if game.getCurrentWord() == "":
        game.correctGuesses = []
        game.gameEvent_startNextRound()

    if request.method == 'POST':
        lastUserGuess = ""
        currentProgress = "" # e.g. "___ ___  A  ___"

        # process user guess and update state
        if request and request.form:
            userGuessString = request.form['userGuess']
            if userGuessString != None:
                processedGuessString = userGuessString.lower()
                lastUserGuess = processedGuessString
                lastUserGuess = game.processAttempt(processedGuessString)

        # if game has been won or lost after processing last guess, return to home screen 
        if game.isGameLost():
            game.resetGameState()
            return render_template('_hangman_game_LOSE.html', missedWord = game.lastWord)
        elif game.isGameWon():
            game.resetGameState()
            return render_template('_hangman_game_WIN.html', wordsGuessed = game.correctGuesses)
        else:
            # Otherwise, refresh UI with latest progress
            for i in range(len(game.getProgress())):
                if game.getProgress()[i] == ".":
                    currentProgress += " ___  "
                else:
                    currentProgress += (" " + game.getProgress()[i].upper() + "  ")
                    
            # re-render page
            return render_template('_hangman_game.html', 
                guessesRemaining=game.getGuessesRemaining(), 
                guessesThisRound=game.getGuessesThisRound(), 
                roundNumber=game.getRoundNumber(), 
                lettersInWord=game.getLettersInWord(),
                lastGuess = lastUserGuess,
                currentProgress = currentProgress,
                incorrectGuesses = game.getIncorrectGuesses(),
                errorMessage = game.displayError,
                debug_currentWord=game.getCurrentWord())

# View rules
@hangmanApp.route('/rules', methods = ['POST', 'GET'])
def viewRules():
    if request.method == 'POST':
        return render_template('_hangman_rules.html')

# Go to settings
@hangmanApp.route('/settings', methods = ['POST', 'GET'])
def goToSettings():
    if request.method == 'POST':
        if request.form:
            if request.form.get('settingShowCorrectLetters') == 'on':
                game.showCorrectLetters = True
            else:
                game.showCorrectLetters = False

            if request.form.get('settingShowContainedLetters') == 'on':
                game.showContainedLetters = True
            else:
                game.showContainedLetters = False

            if request.form.get('settingPreventInvalidWords') == 'on':
                game.preventInvalidWords = True
            else:
                game.preventInvalidWords = False

            if request.form.get('settingPreventUsedLetters') == 'on':
                game.preventUsedLetters = True
            else:
                game.preventUsedLetters = False

            if request.form.get('settingUseTimeLimit') == 'on':
                game.useTimeLimit = True
            else:
                game.useTimeLimit = False

            if request.form.get('settingTutorialMode') == 'on':
                game.tutorialMode = True
            else:
                game.tutorialMode = False

    if request.method == 'POST':
        return render_template('_hangman_settings.html',
            settingShowCorrectLetters = game.showCorrectLetters,
            settingShowContainedLetters = game.showContainedLetters,
            settingPreventInvalidWords = game.preventInvalidWords,
            settingPreventUsedLetters = game.preventUsedLetters,
            settingUseTimeLimit = game.useTimeLimit,
            settingTutorialMode = game.tutorialMode)

@hangmanApp.route('/restoreDefaultSettings', methods = ['POST', 'GET'])
def restoreDefaultSettings():
    game.showCorrectLetters = game.showContainedLettersDefault
    game.showContainedLetters = game.showContainedLettersDefault
    game.preventInvalidWords = game.preventInvalidWordsDefault
    game.preventUsedLetters = game.preventUsedLettersDefault
    game.useTimeLimit = game.useTimeLimitDefault
    game.tutorialMode = game.tutorialModeDefault

    if request.method == 'POST':
        return render_template('_hangman_settings.html',
            settingShowCorrectLetters = game.showCorrectLetters,
            settingShowContainedLetters = game.showContainedLetters,
            settingPreventInvalidWords = game.preventInvalidWords,
            settingPreventUsedLetters = game.preventUsedLetters,
            settingUseTimeLimit = game.useTimeLimit,
            settingTutorialMode = game.tutorialMode)
            