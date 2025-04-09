# general variables for the game settings to be used by other files
# by Hasan Alwazzan (5640356)

#import libraries
import json

class GameSettings:
    def __init__(self):
        self.turn_time_limit = 15
        self.max_cards = 15
        self.word_length = 3
        self.start_cards_number = 7 # MIGHT CHANGE
        self.default_difficulty = "medium" # MIGHT REMOVE
        self.words_file_name = "word_frequencies_json.txt"
        self.words_and_frequencies = self.load_words_and_frequencies()
        self.words = self.get_words()

    def load_words_and_frequencies(self) -> dict[str, int]:
        with open(self.words_file_name, "r") as file:
            words_and_frequencies = json.loads(file.readline())
            return words_and_frequencies

    def get_words(self) -> set[str]:
        #............. # using a set for faster lookup
        words = set((filter(lambda word: len(word) == self.word_length, self.words_and_frequencies.keys())))
        return words