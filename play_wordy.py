
from wordy import Wordy
from random import randint
from player import Player

def random_next_guess(words, guess_hints):
    """This is a terrible way to guess a word."""
    return words[randint(0, len(words)-1)]

def a_simple_guess_function_template(words, guess_hints):
    """Pick a word to guess using the list of words and guess results in guess_hints.
    This function is run until a wordy game is completed. The guess_hints are updated each run with all previous guess hints.

    Keyword arguments:
    words       -- The full list of valid words to guess with
    guess_hints -- A object with the following structure
        guess_hints {
            word: The word guessed
            letter_hints: A list of Wordy clues for each letter
                letter: The letter in the word
                posiiton: The position of the letter in the word
                in_position: A boolean that is true if the letter is in the correct position. (Green!)
                in_solution: A boolean that is true if the letter is in the solution but not in the correct position. (Yellow!)
        }
    """
    fancy_wordy_dataframe = get_fancy_guess_hints_dataframe(guess_hints)
    only_valid_words = fancy_wordy_dataframe[fancy_wordy_dataframe.is_still_valid == True]
    pick_the_first_valid_word = only_valid_words.word.iloc[0]
    return pick_the_first_valid_word

###############################################################################
########################## USEFUL FUNCTIONS! ##################################
###############################################################################


def get_previous_guesses(guess_hints):
    """Returns a list of the previous guesses.

    Keyword arguments:
        guess_hints -- The guess_hint objects that outline results of previous guesses.
    """
    if len(guess_hints) == 0:
        return []
    return [g.word for g in guess_hints]


def get_known_letters(guess_hints):
    """Returns a set of known letters in the solution. Does not account for position.

    Keyword arguments:
        guess_hints -- The guess_hint objects that outline results of previous guesses.
    """
    if len(guess_hints) == 0:
        return []

    # Unique set of letters known to be in the solution
    known_letters = set()
    for guess in guess_hints:
        for hint in guess.letter_hints:
            if hint.in_solution:
                known_letters.add(hint.letter)
    return known_letters


def get_known_positions(guess_hints):
    """Returns a list of known letters in the correct index position.

    Keyword arguments:
        guess_hints -- The guess_hint objects that outline results of previous guesses.
    """
    if len(guess_hints) == 0:
        return []
    known_positions = ['' for l in guess_hints[0].word]
    for guess in guess_hints:
        for lh in guess.letter_hints:
            if lh.in_position:
                known_positions[lh.position] = lh.letter
    return known_positions


def get_fancy_guess_hints_dataframe(guess_hints):
    """Returns a dataframe of all the dictionary words and some useful columns to track guesses and what remaining words are valid.

    Keyword arguments:
        guess_hints -- The guess_hint objects that outline results of previous guesses.
    """
    # Get dataframe with all dictionary words
    words = Wordy.get_dataframe()

    # Capture the word length being used
    word_length = len(words.word.loc[0])

    # Create a 'guessed' column and mark those guessed already as True
    words['guessed'] = False

    # Add a column to track words that are still valid to guess
    words['is_still_valid'] = True

    if len(guess_hints) > 0:
        # Get some info on previous guesses
        words_guessed = get_previous_guesses(guess_hints)
        known_letters = get_known_letters(guess_hints)
        known_letter_positons = get_known_positions(guess_hints)

        # Update guessed words
        words.loc[words.word.isin(words_guessed), 'guessed'] = True
        words.loc[words.word.isin(words_guessed), 'is_still_valid'] = False

        # From known letters that are some place in the solution, flag words that are no longer valid
        for letter in known_letters:
            words.loc[words.word.str.contains(
                letter) == False, 'is_still_valid'] = False

        # From known letter positions, flag words that are no longer valid
        for i, letter in enumerate(known_letter_positons):
            if letter != '':
                words.loc[words[f'pos_{i}'] !=
                          letter, 'is_still_valid'] = False

    # Reorder the dataframe to make it pretty
    column_order = ['word', 'is_still_valid', 'guessed'] + \
        [f'pos_{i}' for i in range(word_length)]
    words = words[column_order]

    # TODO: Double letters :D
    # TODO: This is probably what takes the most time each iteration, better to just reset the dataframe once per game. Better to move this into either the Player or Wordy.
    return words

if __name__ == '__main__':
    # Make a player and give it a way to guess!
    p = Player(a_simple_guess_function_template, tries=10)
