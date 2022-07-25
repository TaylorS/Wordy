from pathlib import Path
from random import randint
from collections import namedtuple

LetterHint = namedtuple('LetterHint', ['letter', 'color', 'position', 'in_position', 'in_solution'])

class colors:
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    WHITE = '\u001b[37m'

class Wordy(object):
    def __init__(self, max_guesses=6) -> None:
        # Game setup
        self.words=self.get_dictionary()
        self.max_guesses=max_guesses
        self._solution=self.get_random_word(self.words)
        self.game_state='playing'

        # Guess management
        self.guess_count=0
        self.guesses=[]
        self.guess_attempts=0
    
    @staticmethod
    def get_dictionary(word_length=5):
        filename = Path('words.txt')
        words = list(set(x.strip().upper() for x in open(filename) if len(x.strip().upper()) == word_length))
        return words

    @staticmethod
    def get_random_word(words):
        return words[randint(0,len(words)-1)]    

    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, word):
        self._solution = self.validate_guess(word)

    def guess_word(self, guess):
        # Guess attempt counter to prevent infinite loops.
        self.guess_attempts += 1
        if self.guess_attempts > 50:
            print('Attempt limit hit, game lost.')
            self.game_state = 'lost'
        # Check if word is valid
        _cleansed_guess = self.validate_guess(guess)
        if not _cleansed_guess:
            return None

        # If word is valid
        self.guess_count += 1
        self.guesses.append(_cleansed_guess)

        # Check word agianst solution
        if _cleansed_guess == self.solution:
            print(f'Guess: {self.get_colorized_guess_str(guess)}')
            print('You got it!')
            self.game_state = 'win'
        else:
            print(f'Guess: {self.get_colorized_guess_str(guess)} - Nope!')
            self.check_state()
            return self.get_letter_hints
    
    def get_letter_hints(self, guess):
        letter_hints = []

        # Get letter counts for double letters
        solution_counts = self.get_letter_counts(self.solution)
        guess_counts = self.get_letter_counts(guess)

        for i, letter in enumerate(guess):
                # In solution and current position is correct
            if self.solution[i] == letter:
                letter_hints.append(LetterHint(letter, colors.GREEN, i, True, True))
            elif letter in self.solution:
                # Letter is in the solution, handle double letters
                if solution_counts[letter] > 1:
                    # This letter is in the solution twice
                    letter_hints.append(LetterHint(letter, colors.YELLOW, i, False, True))
                elif guess_counts[letter] > 1:
                    # In guess twice but solution only once
                    letter_hints.append(LetterHint(letter, colors.WHITE, i, False, True))
                else:
                    # In guess once and in solution once
                    letter_hints.append(LetterHint(letter, colors.YELLOW, i, False, True))
            else:
                # Not in solution
                letter_hints.append(LetterHint(letter, colors.WHITE, i, False, False))
        # Reset terminal text color to white at the end of the word.
        return letter_hints
    
    @staticmethod
    def get_letter_counts(word):
        letter_counts = dict.fromkeys(word, 0)
        for l in word:
            letter_counts[l] += 1
        return letter_counts

    def get_colorized_guess_str(self, guess):
        lh = self.get_letter_hints(guess)
        guess_str = ''
        for l in lh:
            guess_str += l.color + l.letter
        return guess_str + colors.WHITE

    def check_state(self):
        if self.guess_count >= self.max_guesses:
            print("Awful!")
            self.game_state = 'lost'
       
    def validate_guess(self, word):
        _cleansed_guess = word.upper()
        # Check there are no numbers and no special characters
        if not _cleansed_guess.isalpha():
            return False
        
        # Check word length is exactly 5 letters 
        if len(_cleansed_guess) != 5:
            return False
        
        # Check the word hasn't already been guessed.
        if _cleansed_guess in self.guesses:
            print(f'Already guessed {_cleansed_guess}. Pick a new word.')
            return False

        # Check if word is in word list
        if _cleansed_guess in self.words:
            return _cleansed_guess
        else:
            print(f'{_cleansed_guess} not found, try agian.')
            return False


def run_tests():
    # Run simple tests to see that things generally work

    debug = True
    # Guess random words
    game = Wordy()
    words = Wordy.get_dictionary()
    while (game.game_state == 'playing'):
        if debug:
            guess = Wordy.get_random_word(words)
        else:
            guess = input('Guess a word: ')
        game.guess_word(guess)
    
    # Guess fixed guesses and solution to failure
    test_guesses = ['WORDY', 'ABACK', 'ABASE', 'ABATE', 'ABATE', 'ABBEY', 'ABBOT']
    game = Wordy()
    words = Wordy.get_dictionary()
    loop_count = 0
    while (game.game_state == 'playing'):
        if debug:
            if loop_count >= len(test_guesses):
                break
            guess = test_guesses[loop_count]
        else:
            guess = input('Guess a word: ')
        game.guess_word(guess)
        loop_count += 1
    

    # Guess fixed guesses and solution to success
    test_guesses = ['WORDY', 'ABACK']
    game = Wordy()
    game.solution = 'ABACK'
    words = Wordy.get_dictionary()
    loop_count = 0
    while (game.game_state == 'playing'):
        if debug:
            if loop_count >= len(test_guesses):
                break
            guess = test_guesses[loop_count]
        else:
            guess = input('Guess a word: ')
        game.guess_word(guess)
        loop_count += 1


     # Guess fixed guesses and solution to success
    test_guesses = ['CRANE', 'SMART', 'START', 'STABS', 'STTTS', 'STATS']
    game = Wordy()
    game.solution = 'STATS'
    words = Wordy.get_dictionary()
    loop_count = 0
    while (game.game_state == 'playing'):
        if debug:
            guess = test_guesses[loop_count]
        else:
            guess = input('Guess a word: ')
        game.guess_word(guess)
        loop_count += 1
    
if __name__ == '__main__':
    run_tests()
