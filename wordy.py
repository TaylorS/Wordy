from pathlib import Path
from random import randint
from dataclasses import dataclass
import pandas as pd


@dataclass
class LetterHint:
    letter: str
    color: str
    position: int
    in_position: bool
    in_solution: bool


class colors:
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    WHITE = '\u001b[37m'


class Wordy(object):
    def __init__(self, max_guesses=6, silent_mode=True) -> None:
        # Game setup
        self.words = self.get_dictionary()
        self.max_guesses = max_guesses
        self._solution = self.get_random_word(self.words)
        self.game_state = 'playing'
        self.silent_mode = silent_mode

        # Guess management
        self.guess_count = 0
        self.guesses = []
        self.guess_attempts = 0

    @staticmethod
    def get_dictionary(word_length=5):
        filename = Path('words.txt')
        words = list(set(x.strip().upper() for x in open(filename)
                     if len(x.strip().upper()) == word_length))
        return words

    @staticmethod
    def get_dataframe(word_length=5):
        words = Wordy.get_dictionary(word_length)
        df = pd.DataFrame.from_records(words)
        columns = []
        for i in range(word_length):
            columns.append(f'pos_{i}')
        df.columns = columns
        df['word'] = df.apply(lambda row: ''.join([row[col]
                              for col in columns]), axis=1)
        return df

    @staticmethod
    def get_random_word(words: 'list[str]'):
        return words[randint(0, len(words)-1)]

    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, word: str) -> None:
        self._solution = self.validate_guess(word)

    def guess_word(self, guess: str):
        # Guess attempt counter to prevent infinite loops.
        self.guess_attempts += 1
        if self.guess_attempts > 50:
            self.log('Attempt limit hit, game lost.')
            self.game_state = 'lost'
        # Check if word is valid
        _cleansed_guess = self.validate_guess(guess)
        if not _cleansed_guess:
            return None

        # If word is valid
        self.guess_count += 1
        self.guesses.append(_cleansed_guess)

        # Create guess object to return to palyer
        guess_results = Guess(
            _cleansed_guess, self.get_letter_hints(_cleansed_guess))

        # Check word agianst solution
        if _cleansed_guess == self.solution:
            self.log(f'Guess: {guess_results}')
            self.log('You got it!')
            self.game_state = 'win'
        else:
            self.log(f'Guess: {guess_results} - Nope!')
            self.check_state()
            return guess_results

    def get_letter_hints(self, guess: str):
        letter_hints = []

        # Get letter counts for double letters
        solution_counts = self.get_letter_counts(self.solution)
        guess_counts = self.get_letter_counts(guess)

        for i, letter in enumerate(guess):
            # In solution and current position is correct
            if self.solution[i] == letter:
                letter_hints.append(LetterHint(
                    letter, colors.GREEN, i, True, True))
            elif letter in self.solution:
                # Letter is in the solution, handle double letters
                if solution_counts[letter] > 1:
                    # This letter is in the solution twice
                    letter_hints.append(LetterHint(
                        letter, colors.YELLOW, i, False, True))
                elif guess_counts[letter] > 1:
                    # In guess twice but solution only once
                    letter_hints.append(LetterHint(
                        letter, colors.WHITE, i, False, True))
                else:
                    # In guess once and in solution once
                    letter_hints.append(LetterHint(
                        letter, colors.YELLOW, i, False, True))
            else:
                # Not in solution
                letter_hints.append(LetterHint(
                    letter, colors.WHITE, i, False, False))
        # Reset terminal text color to white at the end of the word.
        return letter_hints

    @staticmethod
    def get_letter_counts(word: str) -> dict:
        letter_counts = dict.fromkeys(word, 0)
        for l in word:
            letter_counts[l] += 1
        return letter_counts

    def check_state(self) -> None:
        if self.guess_count >= self.max_guesses:
            self.log("Awful!")
            self.game_state = 'lost'

    def validate_guess(self, word: str) -> str:
        _cleansed_guess = word.upper()
        # Check there are no numbers and no special characters
        if not _cleansed_guess.isalpha():
            return False

        # Check word length is exactly 5 letters
        if len(_cleansed_guess) != 5:
            return False

        # Check the word hasn't already been guessed.
        if _cleansed_guess in self.guesses:
            self.log(f'Already guessed {_cleansed_guess}. Pick a new word.')
            return False

        # Check if word is in word list
        if _cleansed_guess in self.words:
            return _cleansed_guess
        else:
            self.log(f'{_cleansed_guess} not found, try agian.')
            return False

    def log(self, message: str):
        if not self.silent_mode:
            print(message)


class Guess(object):

    def __init__(self, word: str, letter_hints: 'list[LetterHint]'):
        self.word = word
        self.letter_hints = letter_hints

    def __repr__(self) -> str:
        repr = f'{self.word}: '
        for lh in self.letter_hints:
            repr += f' letter: {lh.letter} - position: {lh.position} - in_position: {lh.in_position} - in_solution: {lh.in_solution}\n'
        return repr

    def __str__(self) -> str:
        guess_str = ''
        for l in self.letter_hints:
            guess_str += l.color + l.letter
        return guess_str + colors.WHITE


def run_tests():
    # Run simple tests to see that things generally work

    debug = True
    # Guess random words
    game = Wordy(silent_mode=False)
    words = Wordy.get_dictionary()
    while (game.game_state == 'playing'):
        if debug:
            guess = Wordy.get_random_word(words)
        else:
            guess = input('Guess a word: ')
        game.guess_word(guess)

    # Guess fixed guesses and solution to failure
    test_guesses = ['WORDY', 'ABACK', 'ABASE',
                    'ABATE', 'ABATE', 'ABBEY', 'ABBOT']
    game = Wordy(silent_mode=False)
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
    game = Wordy(silent_mode=False)
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
    game = Wordy(silent_mode=False)
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

    # Guess limit test and test silent mode
    test_guesses = ['BLERG']
    game = Wordy(silent_mode=True)
    words = Wordy.get_dictionary()
    while (game.game_state == 'playing'):
        if debug:
            guess = test_guesses[0]
        else:
            guess = input('Guess a word: ')
        game.guess_word(guess)
    print('Infinite loop terminated.')


if __name__ == '__main__':
    run_tests()
