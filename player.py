from wordy import Wordy

class Player(object):

    def __init__(self, guesser, tries=1):
        self.words = Wordy.get_dictionary()
        self.wins=0
        self.tries = tries
        self.play_game(guesser)

    def play_game(self, guesser):
        for _ in range(self.tries):
            game = Wordy(silent_mode=True)
            guess_hints = []
            while (game.game_state == 'playing'):
                guess = guesser(self.words, guess_hints)
                guess_hints.append(game.guess_word(guess))
            if game.game_state == 'win':
                self.wins += 1
        print(f'Guesser won {self.wins} out of {self.tries} tries.')
        return self.wins
