from tkinter import *
from tkinter.ttk import *
import tkinter
from enum import Enum

class Screen(Enum):
    HOME = 1
    SETTINGS = 2
    RULES = 3
    PLAY = 4

class HangmanGameWindow:
    def __init__(self, windowTitle, game):
        self.game = game
        self.gameWindow = Tk()
        self.currentScreen = Screen.HOME
        self.gameWindow.geometry("400x400")
        self.gameWindow.minsize(400, 400)
        self.gameWindow.maxsize(400, 400)
        self.gameWindow.title(windowTitle)
        self.gameWindowCanvas = tkinter.Canvas(self.gameWindow, background="white")
        self.gameWindowCanvas.pack(fill="both", expand=True)

        self.gameWindow.bind('<Return>', self.validateUserGuess)

        # Home screen
        self.startGameButton = None
        self.viewRulesButton = None
        self.settingsButton = None

        # Game screen
        self.gameRoundLabel = None
        self.gameAttemptsLabel = None
        self.wordProgressLabel = None
        self.userGuessText = None
        self.badGuessInfoLabel = None

        # Settings screen

        # Rules screen
        self.ruleAText = None
        self.ruleBText = None
        self.ruleCText = None

        # Shared
        self.backToHomeButton = None

        # On window creation, start at home screen
        self.displayHomeScreen()

    def validateUserGuess(self, arg):
        if self.currentScreen == Screen.PLAY:
            userGuess = self.userGuessText.get("1.0", 'end-2c')
            userGuess.replace(" ", "")
            error = self.game.processAttempt(userGuess.lower(), self)
            self.userGuessText.delete("1.0", END)
            self.displayGameScreen()
            #print("Someone hit enter!")

    # Show home screen
    def displayHomeScreen(self):
        self.game.resetGameState()

        self.currentScreen = Screen.HOME
        self.hideAllScreenWidgets()

        if self.startGameButton == None:
            self.startGameButton = Button(self.gameWindow, text="Start New Game", command=self.startNewGame)

        if self.viewRulesButton == None:
            self.viewRulesButton = Button(self.gameWindow, text="View Rules", command=self.displayRuleScreen)

        if self.settingsButton == None:
            self.settingsButton = Button(self.gameWindow, text="Settings", command=self.displaySettings)

        self.startGameButton.pack()
        self.viewRulesButton.pack()
        self.settingsButton.pack()
        # update window
        self.gameWindow.mainloop()

    # Hide home screen
    def hideHomeScreenWidgets(self):
        if self.startGameButton != None:
            self.startGameButton.forget()
        if self.viewRulesButton != None:
            self.viewRulesButton.forget()
        if self.settingsButton != None:
            self.settingsButton.forget()

    # Show rules
    def displayRuleScreen(self):
        self.currentScreen = Screen.RULES
        self.hideAllScreenWidgets()

        if self.ruleAText == None:
            self.ruleAText = Label(self.gameWindow, text="Rule 1 showing now\n")

        if self.ruleBText == None:
            self.ruleBText = Label(self.gameWindow, text="Rule 2 showing now\n")

        if self.ruleCText == None:
            self.ruleCText = Label(self.gameWindow, text="Rule 3 showing now\n")

        if self.backToHomeButton == None:
            self.backToHomeButton = Button(self.gameWindow, text="Back", command=self.displayHomeScreen)

        self.ruleAText.pack()
        self.ruleBText.pack()
        self.ruleCText.pack()
        self.backToHomeButton.pack()
        # update window
        self.gameWindow.mainloop()

    # Hide rules screen
    def hideRulesScreenWidgets(self):
        if self.ruleAText != None:
            self.ruleAText.forget()
        if self.ruleBText != None:
            self.ruleBText.forget()
        if self.ruleCText != None:
            self.ruleCText.forget()
        if self.backToHomeButton != None:
            self.backToHomeButton.forget()

    # show settings screen
    def displaySettings(self):
        self.currentScreen = Screen.SETTINGS
        self.hideAllScreenWidgets()

        if self.backToHomeButton == None:
            self.backToHomeButton = Button(self.gameWindow, text="Back", command=self.displayHomeScreen)

        self.backToHomeButton.pack()
        # update window
        self.gameWindow.mainloop()

    # hide settings screen
    def hideSettingsWidgets(self):
        if self.backToHomeButton != None:
            self.backToHomeButton.forget()

    def startNewGame(self):
        self.game.pickWordsForNextRound()
        self.displayGameScreen()

    def displayGameScreen(self):
        self.currentScreen = Screen.PLAY
        self.hideAllScreenWidgets()

        if self.gameRoundLabel == None:
            self.gameRoundLabel = Label(self.gameWindowCanvas, text="Round " + str(self.game.getRoundNumber()))
        self.gameRoundLabel.config(text="Round " + str(self.game.getRoundNumber()))

        if self.gameAttemptsLabel == None:
            self.gameAttemptsLabel = Label(self.gameWindowCanvas, text="Attempts Remaining: " + str(self.game.getGuessesRemaining()))
        self.gameAttemptsLabel.config(text="Attempts Remaining: " + str(self.game.getGuessesRemaining()))

        if self.wordProgressLabel == None:
            self.wordProgressLabel = Label(self.gameWindowCanvas, text="___ ___ ___ ___")
        wordProgressText = ""
        for i in range (self.game.getLettersInWord()):
            if self.game.currentProgress[i] != ".":
                wordProgressText += " " + self.game.currentProgress[i].upper() + "  "
            else:
                wordProgressText += "___ "
        self.wordProgressLabel.config(text=wordProgressText)

        if self.userGuessText == None:
            self.userGuessText = Text(self.gameWindowCanvas, height=1, width=self.game.getLettersInWord(), bg="#d6c6c5")
        self.userGuessText.config(width=self.game.getLettersInWord())
        self.userGuessText.delete("1.0", END)

        if self.badGuessInfoLabel == None:
            self.badGuessInfoLabel = Label(self.gameWindowCanvas, text="")
        if self.game.displayError != "":
            self.badGuessInfoLabel.config(text=self.game.displayError)
        else:
            self.badGuessInfoLabel.config(text="")

        if self.backToHomeButton == None:
            self.backToHomeButton = Button(self.gameWindow, text="Back", command=self.displayHomeScreen)

        self.gameRoundLabel.pack()
        self.gameAttemptsLabel.pack()
        self.wordProgressLabel.pack()
        self.userGuessText.pack()
        self.badGuessInfoLabel.pack()
        self.backToHomeButton.pack()
        self.gameWindow.mainloop()

    def hideGameScreenWidgets(self):
        if self.gameRoundLabel != None:
            self.gameRoundLabel.forget()
        if self.gameAttemptsLabel != None:
            self.gameAttemptsLabel.forget()
        if self.backToHomeButton != None:
            self.backToHomeButton.forget()
        if self.wordProgressLabel != None:
            self.wordProgressLabel.forget()
        if self.userGuessText != None:
            self.userGuessText.forget()
        if self.badGuessInfoLabel != None:
            self.badGuessInfoLabel.forget()

    # Hide everything
    def hideAllScreenWidgets(self):
        self.hideHomeScreenWidgets()
        self.hideRulesScreenWidgets()
        self.hideSettingsWidgets()
        self.hideGameScreenWidgets()

def createGameWindow(game):
    gameWindow = HangmanGameWindow("Hangman: Wordle Edition", game)