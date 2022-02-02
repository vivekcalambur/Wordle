import colored
import random
from collections import Counter
from enum import Enum


class Colors(Enum):
    GRAY = 1
    YELLOW = 2
    GREEN = 3


class Wordle:
    word = None
    allowed_words = set()
    defaultColor = None
    guessCount = 0


    def __init__(self):
        with open('wordle-answers-alphabetical.txt') as f:
            words = f.read().splitlines() 
            self.allowed_words.update(words)
            self.word = random.choice(words)

        with open('wordle-allowed-guesses.txt') as f:
            words = f.read().splitlines() 
            self.allowed_words.update(words)

        self.defaultColor = colored.fg(6)

    
    def game(self):
        maxGuesses = 6
        while self.guessCount < maxGuesses:
            userGuess = input(self.defaultColor + 'Guess a 5 letter word: ').strip().lower()
            if len(userGuess) != 5:
                print(self.defaultColor + 'Please enter a 5 letter word')
            elif userGuess not in self.allowed_words:
                print(self.defaultColor + 'Please enter a valid English word')
            else:
                guessResult = self.guess(userGuess)
                self.printResult(guessResult, userGuess)
                self.guessCount += 1
                if all(color == Colors.GREEN for color in guessResult):
                    print(self.defaultColor + f'Congratulations, you guessed the word in {str(self.guessCount)} tries!')
                    return

        print(self.defaultColor + f'Unfortunately you did not guess the word in 6 tries. The correct answer was: {self.word}')


    def guess(self, guessWord):
        result = []
        counter = Counter(self.word)

        for i, letter in enumerate(guessWord):
            if letter == self.word[i]:
                result.append(Colors.GREEN)
                counter[letter] = counter[letter] - 1
            elif letter in self.word and counter[letter] > 0:
                result.append(Colors.YELLOW)
                counter[letter] = counter[letter] - 1
            else:
                result.append(Colors.GRAY)

        return result


    def printResult(self, guessResult, guessWord):
        gray = colored.fg(7)
        yellow = colored.fg(3)
        green = colored.fg(2)

        printStr = ''
        for color, letter in zip(guessResult, guessWord):
            if color == Colors.GRAY:
                printStr += (gray + letter)
            elif color == Colors.YELLOW:
                printStr += (yellow + letter)
            elif color == Colors.GREEN:
                printStr += (green + letter)
            else:
                raise RuntimeError('Invalid color')

        print(printStr)
        colored.fg(5)


w = Wordle()
w.game()
