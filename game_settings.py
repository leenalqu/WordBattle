# general variables for the game settings to be used by other files
# by Hasan Alwazzan (5640356)

# SEE CAPITAL COMMENTS
#import library
import json


class GameSettings:
    """
    A class that stores the game settings as variables.

    Attributes
    ----------
    turn_time_limit: int
        - The maximum amount of time a player can take to play their turn.

    max_cards: int
        - The amount of cards that if you exceed, you lose the game.

    word_length: int
        - The length of the word that the players have to change.

    start_cards_number: int
        - How many cards each player starts with.

    default_difficulty: str
        - The default difficulty of the game.

    words_file_name: str
        - The name of the file that contains the data for the words.

    word_frequencies: dict[str, int]
        - All words & their relative frequencies in % (i.e. how common they are in the English language).

    words: set[str]
        - All words that can be played in the game (i.e. words that are of the specified length in word_length).

    Methods
    -------
    load_word_frequencies():
        - Return a dictionary of all words & their relative frequencies (i.e. how common they are) from words_file_name.

    get_words():
        - Return a set of all the words that are allowed to be played in the game.
    """

    def __init__(self):
        """
        Construct all the necessary attributes for the GameSettings object.
        """
        self.turn_time_limit = 15 # the maximum amount of time a player can take to play their turn
        self.max_cards = 15 # the amount of cards that if you exceed, you lose the game
        self.word_length = 3 # the length of the word that the players have to change
        self.start_cards_number = 7 # how many cards each player starts with
        self.default_difficulty = "medium" # the default difficulty of the game # MIGHT NOT NEED THIS AND REMV FROM DOC STR
        self.words_file_name = "data/word_frequencies_json.txt"  # name of the file that contains the data for the words
        # dictionary for all words & their relative frequencies in % (i.e. how common they are in the English language)
        self.word_frequencies = self.load_word_frequencies()
        # all real words that can be played in the game (all are of the length specified in self.word_length)
        self.words = self.get_words()

    def load_word_frequencies(self) -> dict[str, int]:
        """Return a dictionary of all words and their frequencies from the words file (i.e. self.words_file_name)."""
        with open(self.words_file_name, "r") as file: # opens the words file in read mode (and closes it when it's done)
            word_frequencies = json.loads(file.readline()) # loads the file from json format to a python dictionary
            return word_frequencies

    def get_words(self) -> set[str]:
        """Return all the words that are allowed to be played in the game as a set."""
        # from the words in the word_frequency dictionary, filter out all words that are not of the specified length
        # using a set for faster lookup
        words = set((filter(lambda word: len(word) == self.word_length, self.word_frequencies.keys())))
        return words


game_settings = GameSettings() # initiate class object (to be called by other modules)