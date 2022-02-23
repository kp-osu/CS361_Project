from random import randrange

fourLetter, fiveLetter, sixLetter, sevenLetter, eightLetter = [], [], [], [], []

with open('GameWordList.txt', 'r') as file:
    for line in file:
        word = line.strip()
        if len(word) == 4:
            fourLetter.append(word)
        elif len(word) == 5: 
            fiveLetter.append(word)
        elif len(word) == 6:
            sixLetter.append(word)
        elif len(word) == 7:
            sevenLetter.append(word)
        elif len(word) == 8:
            eightLetter.append(word)

four = randrange(len(fourLetter))
five = randrange(len(fiveLetter))
six = randrange(len(sixLetter))
seven = randrange(len(sevenLetter))
eight = randrange(len(eightLetter))

file = open("wordList.txt", "w")
file.write(fourLetter[four] + "\n")
file.write(fiveLetter[five] + "\n")
file.write(sixLetter[six] + "\n")
file.write(sevenLetter[seven] + "\n")
file.write(eightLetter[eight])
file.close