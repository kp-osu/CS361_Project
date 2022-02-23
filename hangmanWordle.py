"""
Author: Kevin Peterson
Class: CS361: Software Engineering I
Date: 2/6/22
Description: Hangman Web App core logic
"""

import os.path
# Imports
import random
import time
import hangmanGUI


# --------------------------------------------------------------------------------------------
# Game Logic
# --------------------------------------------------------------------------------------------

class GameTimer:
    def __init__(self):
        self.timeOfCreation = time.time()

    def getTimeElapsed(self):
        return time.time() - self.timeOfCreation()

class Game:
    def __init__(self):
        # Game state
        self.round = 0
        self.currentWord = ""
        self.guessesUsed = 0
        self.lettersPerRound = [4, 5, 6, 7, 8]
        self.guessesPerRound = [4, 5, 6, 7, 8]
        self.timeLimitPerRound = [60, 75, 90, 115, 130]
        self.incorrectGuesses = []
        self.currentProgress = []
        self.dictionary = [[], [], [], [], []]
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
        with open('GameWordList.txt', 'r') as file:
            for line in file:
                word = line.strip()
                self.dictionary[len(word)-4].append(word)

    # parse the wordList.txt file and get the word needed (based on round)
    def parseAndGetWordsForNextRound(self):
        wordsThisGame = []
        with open('wordList.txt', 'r') as file:
            for line in file:
                word = line.strip()
                wordsThisGame.append(word)

        return wordsThisGame[self.round].lower()

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
        self.timeLimitPerRound = [60, 75, 90, 115, 130]
        self.incorrectGuesses = []
        self.currentProgress = []
        self.timer = None
        self.displayError = ""
        self.gameWon = False
        self.gameLost = False

    # ----------------------
    # Game events
    # ----------------------

    # process user guess attempt (userGuessString all lowercase)
    def processAttempt(self, userGuessString, gameWindow):
        # validate attempt (dont ding user for bad guess)
        if len(userGuessString) < game.getLettersInWord():
            self.displayError = "'" + userGuessString + "'" + " has too few letters, please try again."
            return self.displayError
        elif len(userGuessString) > game.getLettersInWord():
            self.displayError = "'" + userGuessString + "'" + " has too many letters, please try again."
            return self.displayError
        elif not userGuessString in self.dictionary[self.round]:
            self.displayError = "'" + userGuessString + "'" + " was not found in game dictionary, please try again."
            return self.displayError
        elif userGuessString in self.incorrectGuesses:
            self.displayError = "'" + userGuessString + "'" + " has already been tried, please try again."
            return self.displayError
        else:
            # update current progress for display
            self.displayError = ""

            for i in range(len(self.currentWord)):
                if self.currentWord[i] == userGuessString[i]:
                    self.currentProgress[i] = self.currentWord[i]

            # handle correct vs. incorrect guess
            if userGuessString == self.currentWord.lower():
                self.gameEvent_onCorrectGuess(gameWindow)
            else:
                self.gameEvent_onIncorrectGuess(userGuessString, gameWindow)

            return ""

    # method to start a new game round
    def pickWordsForNextRound(self):
        self.currentWord = self.parseAndGetWordsForNextRound()
        print("Chosen word for next round is: " + self.currentWord)
        self.lastWord = self.currentWord
        self.currentProgress = []
        for i in range(len(self.currentWord)):
            self.currentProgress.append(".")

        #self.timer = GameTimer()

    # on correct guess, progress to next round
    def gameEvent_onCorrectGuess(self, gameWindow):
        self.round += 1

        self.correctGuesses.append(self.currentWord)

        if self.round >= len(self.lettersPerRound):
            self.gameEvent_onWinGameComplete(gameWindow)
        else:
            self.guessesUsed = 0
            self.incorrectGuesses = []
            self.guessesThisRound = self.getGuessesThisRound()
            self.pickWordsForNextRound()

    # on incorrect guess
    def gameEvent_onIncorrectGuess(self, userGuessString, gameWindow):
        self.guessesUsed += 1
        self.incorrectGuesses.append(userGuessString)

        if self.guessesUsed >= self.getGuessesThisRound():
            self.gameEvent_onLose(gameWindow)

    # on win entire game
    def gameEvent_onWinGameComplete(self, gameWindow):
        self.gameWon = True
        gameWindow.displayHomeScreen()

    # on fail state - game over
    def gameEvent_onLose(self, gameWindow):
        self.gameLost = True
        gameWindow.displayHomeScreen()


# Create game instance and start first round
game = Game()
hangmanGUI.createGameWindow(game)