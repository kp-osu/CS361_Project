"""
Author: Kevin Peterson
Class: CS361: Software Engineering I
Date: 2/6/22
Description: Hangman Web App GUI logic
"""

from tkinter import *
from tkinter.ttk import *
import tkinter
from PIL import Image, ImageTk
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
        self.gameWindow.geometry("400x280")
        self.gameWindow.minsize(400, 280)
        self.gameWindow.maxsize(400, 280)
        self.gameWindow.title(windowTitle)
        self.gameWindowCanvas = tkinter.Canvas(self.gameWindow, background="white")
        self.gameWindowCanvas.pack(fill="both", expand=True)

        self.gameWindow.bind('<Return>', self.validateUserGuess)

        # Home screen
        self.backgroundImageLabel = None
        self.startGameButton = None
        self.viewRulesButton = None
        self.settingsButton = None

        # Game screen
        self.gameRoundLabel = None
        self.gameAttemptsLabel = None
        self.wordProgressLabel = None
        self.userGuessText = None
        self.badGuessInfoLabel = None
        self.guessesSoFarHeaderLabel = None
        self.guessesSoFarLabel = None

        # Settings screen
        self.difficultyOptionMenu = None
        self.difficultySettingsVar = StringVar(self.gameWindowCanvas)
        self.difficultySettingsVar.set("Normal")
        self.difficultyCurrent = "Normal"
        self.showGuessedWordsActive = IntVar(value=1)
        self.showGuessedWordsCheck = None
        self.friendlyModeActive = IntVar(value=1)
        self.friendlyModeCheck = None
        self.restoreDefaultsButton = None

        # Rules screen
        self.ruleAText = None
        self.ruleBText = None
        self.ruleCText = None

        # Shared
        self.pageTitleLabel = None
        self.backToHomeButton = None
        self.labelStyle = Style()
        self.labelStyle.configure("BW.TLabel", background="white")

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

        if self.backgroundImageLabel == None:
            image = Image.open("Images/hangman_game_wordle.jpg")
            resized_image = image.resize((400, 200), Image.ANTIALIAS)
            background = ImageTk.PhotoImage(resized_image)
            self.backgroundImageLabel = Label(self.gameWindowCanvas, image=background)

        if self.startGameButton == None:
            self.startGameButton = Button(self.gameWindow, text="Start New Game", command=self.startNewGame)

        if self.viewRulesButton == None:
            self.viewRulesButton = Button(self.gameWindow, text="View Rules", command=self.displayRuleScreen)

        if self.settingsButton == None:
            self.settingsButton = Button(self.gameWindow, text="Settings", command=self.displaySettings)

        self.backgroundImageLabel.pack()
        self.startGameButton.pack()
        self.viewRulesButton.pack()
        self.settingsButton.pack()
        # update window
        self.gameWindow.mainloop()

    # Hide home screen
    def hideHomeScreenWidgets(self):
        if self.backgroundImageLabel != None:
            self.backgroundImageLabel.forget()
        if self.pageTitleLabel != None:
            self.pageTitleLabel.forget()
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

        self.pageTitleLabel = Label(self.gameWindowCanvas, justify=LEFT, wraplength=400,text="Rules of the Game", font=("Arial", 14))

        if self.ruleAText == None:
            self.ruleAText = Label(self.gameWindowCanvas, justify=LEFT, wraplength=400, text="1. Guess the word correctly to move onto the next round! Each round, the number of letters in the word will increase by 1.\n\n")

        if self.ruleBText == None:
            self.ruleBText = Label(self.gameWindowCanvas, justify=LEFT, wraplength=400, text="2. Each time you guess incorrectly, you'll lose a guess. Once you've used all your guesses, it's game over! Also, be sure to keep an eye on the clock. If it reaches zero before you've guessed the correct word, it's also game over!\n\n")

        if self.ruleCText == None:
            self.ruleCText = Label(self.gameWindowCanvas, justify=LEFT, wraplength=400, text="3. Letters in the correct positions will be colored green, while letters that are in the word but currently in the wrong position will be colored yellow.\n\n")

        if self.backToHomeButton == None:
            self.backToHomeButton = Button(self.gameWindow, text="Back", command=self.displayHomeScreen)

        self.pageTitleLabel.pack()
        self.ruleAText.pack()
        self.ruleBText.pack()
        self.ruleCText.pack()
        self.backToHomeButton.pack()
        # update window
        self.gameWindow.mainloop()

    # Hide rules screen
    def hideRulesScreenWidgets(self):
        if self.pageTitleLabel != None:
            self.pageTitleLabel.forget()
        if self.ruleAText != None:
            self.ruleAText.forget()
        if self.ruleBText != None:
            self.ruleBText.forget()
        if self.ruleCText != None:
            self.ruleCText.forget()
        if self.backToHomeButton != None:
            self.backToHomeButton.forget()

    # Callbacks for settings menu items
    def showGuessedWordsChecked(self):
        # to get value: self.showGuessedWordsActive.get()
        print("Active: " + str(self.showGuessedWordsActive.get()))

    def showFriendlyModeChecked(self):
        # to get value: self.friendlyModeActive.get()
        print("Active: " + str(self.friendlyModeActive.get()))

    def restoreDefaultSettings(self):
        self.showGuessedWordsActive.set(1)
        self.friendlyModeActive.set(1)
        self.difficultySettingsVar.set("Normal")

    # show settings screen
    def displaySettings(self):
        self.currentScreen = Screen.SETTINGS
        self.hideAllScreenWidgets()

        self.pageTitleLabel = Label(self.gameWindowCanvas, style="BW.TLabel", justify=LEFT, wraplength=400,text="Settings", font=("Arial", 14))

        if self.difficultyOptionMenu == None:
            options = ["Normal","Easy","Normal","Hard"]
            self.difficultySettingsVar.set(self.difficultyCurrent)
            self.difficultyOptionMenu = OptionMenu(self.gameWindowCanvas, self.difficultySettingsVar, *options)

        if self.showGuessedWordsCheck == None:
            self.showGuessedWordsCheck = Checkbutton(self.gameWindowCanvas, text = "Show Guessed Words", variable=self.showGuessedWordsActive, onvalue=1, offvalue=0, command=self.showGuessedWordsChecked)

        if self.friendlyModeCheck == None:
            self.friendlyModeActive = IntVar(value=1)
            self.friendlyModeCheck = Checkbutton(self.gameWindowCanvas, text = "Friendly Mode", variable=self.friendlyModeActive, onvalue=1, offvalue=0, command=self.showFriendlyModeChecked)

        if self.restoreDefaultsButton == None:
            self.restoreDefaultsButton = Button(self.gameWindowCanvas, text="Restore Defaults", command=self.restoreDefaultSettings)

        if self.backToHomeButton == None:
            self.backToHomeButton = Button(self.gameWindow, text="Back", command=self.displayHomeScreen)

        self.pageTitleLabel.pack()
        self.difficultyOptionMenu.pack()
        self.showGuessedWordsCheck.pack()
        self.friendlyModeCheck.pack()
        self.restoreDefaultsButton.pack()
        self.backToHomeButton.pack()

        # update window
        self.gameWindow.mainloop()

    # hide settings screen
    def hideSettingsWidgets(self):
        if self.pageTitleLabel != None:
            self.pageTitleLabel.forget()

        if self.difficultyOptionMenu != None:
            self.difficultyOptionMenu.forget()

        if self.showGuessedWordsCheck != None:
            self.showGuessedWordsCheck.forget()

        if self.friendlyModeCheck != None:
            self.friendlyModeCheck.forget()

        if self.restoreDefaultsButton != None:
            self.restoreDefaultsButton.forget()

        if self.backToHomeButton != None:
            self.backToHomeButton.forget()

    def startNewGame(self):
        difficulty = self.difficultyCurrent
        if self.difficultySettingsVar != None:
            difficulty = self.difficultySettingsVar.get()

        self.game.pickWordsForNextRound(difficulty)
        self.hideAllScreenWidgets()
        self.displayGameScreen()

    def displayGameScreen(self):
        self.currentScreen = Screen.PLAY
        self.hideAllScreenWidgets()

        self.pageTitleLabel = Label(self.gameWindowCanvas, style="BW.TLabel", justify=LEFT, wraplength=400,text="Play!", font=("Arial", 14))

        if self.gameRoundLabel == None:
            self.gameRoundLabel = Label(self.gameWindowCanvas, style="BW.TLabel", text="Round " + str(self.game.getRoundNumber()))
        self.gameRoundLabel.config(text="Round " + str(self.game.getRoundNumber()))

        if self.gameAttemptsLabel == None:
            self.gameAttemptsLabel = Label(self.gameWindowCanvas, style="BW.TLabel", text="Attempts Remaining: " + str(self.game.getGuessesRemaining()))
        self.gameAttemptsLabel.config(text="Attempts Remaining: " + str(self.game.getGuessesRemaining()))

        if self.wordProgressLabel == None:
            self.wordProgressLabel = Label(self.gameWindowCanvas, text="___ ___ ___ ___", style="BW.TLabel")
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
            self.badGuessInfoLabel = Label(self.gameWindowCanvas, style="BW.TLabel", text="")
        if self.game.displayError != "":
            self.badGuessInfoLabel.config(text=self.game.displayError)
        else:
            self.badGuessInfoLabel.config(text="")

        if self.showGuessedWordsActive.get() == 1:
            if self.guessesSoFarHeaderLabel == None:
                self.guessesSoFarHeaderLabel = Label(self.gameWindowCanvas, style="BW.TLabel", justify=LEFT, wraplength=400, text="", font=("Arial", 10))

            if len(self.game.getIncorrectGuesses()) > 0:
                if self.guessesSoFarLabel == None:
                    self.guessesSoFarLabel = Label(self.gameWindowCanvas, style="BW.TLabel", text="")
                guessedText = "Guesses:\n"
                for i in range(len(self.game.getIncorrectGuesses())):
                    guessedText += self.game.getIncorrectGuesses()[i] + "\n"
                self.guessesSoFarLabel.config(text=guessedText)
            else:
                if self.guessesSoFarLabel == None:
                    self.guessesSoFarLabel = Label(self.gameWindowCanvas, style="BW.TLabel", text="")
                self.guessesSoFarLabel.config(text="Guesses:\n")
        else:
            if self.guessesSoFarLabel == None:
                self.guessesSoFarLabel = Label(self.gameWindowCanvas, style="BW.TLabel", text="")
            self.guessesSoFarLabel.config(text="")

        if self.backToHomeButton == None:
            self.backToHomeButton = Button(self.gameWindow, text="Back", command=self.displayHomeScreen)

        self.pageTitleLabel.pack()
        self.gameRoundLabel.pack()
        self.gameAttemptsLabel.pack()
        self.wordProgressLabel.pack()
        self.userGuessText.pack()
        self.badGuessInfoLabel.pack()
        if self.guessesSoFarHeaderLabel != None:
            self.guessesSoFarHeaderLabel.pack()
            self.guessesSoFarLabel.pack()
        self.backToHomeButton.pack()
        self.gameWindow.mainloop()

    def hideGameScreenWidgets(self):
        if self.pageTitleLabel != None:
            self.pageTitleLabel.forget()
        if self.gameRoundLabel != None:
            self.gameRoundLabel.forget()
        if self.gameAttemptsLabel != None:
            self.gameAttemptsLabel.forget()
        if self.guessesSoFarHeaderLabel != None:
            self.guessesSoFarHeaderLabel.forget()
        if self.guessesSoFarLabel != None:
            self.guessesSoFarLabel.forget()
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