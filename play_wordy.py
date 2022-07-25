from wordy import Wordy
from player import Player

def random_next_guess(words, guess_hints):
    # This is a terrible way to guess.
    return Wordy.get_random_word(words)

def a_little_better_way_to_guess(words, guess_hints):
    print(get_previous_guesses(guess_hints))
    # print(get_known_positions(guess_hints))
    return random_next_guess(words, guess_hints)

def get_known_positions(guess_hints):
    if len(guess_hints) == 0:
        return []
    known_positions=['' for l in guess_hints[0].word]
    for guess in guess_hints:
        for lh in guess.letter_hints:
            if lh.in_position:
                known_positions[lh.position] = lh.letter
    return known_positions

def get_previous_guesses(guess_hints):
    if len(guess_hints) == 0:
        return []
    words_guessed=[]
    for guess in guess_hints:
        words_guessed.append(guess.word)
    return words_guessed

def get_known_letters(guess_hints):
    if len(guess_hints) == 0:
        return []
    known_letters=['' for l in guess_hints[0].word]
    raise NotImplementedError

if __name__ == '__main__':
    # Make a player and give it a way to guess!
    p = Player(a_little_better_way_to_guess, tries=1)