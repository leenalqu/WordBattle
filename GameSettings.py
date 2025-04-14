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
    TURN_TIME_LIMIT: int
        - The maximum amount of time a player can take to play their turn.

    MAX_CARDS: int
        - The amount of cards that if you exceed, you lose the game.

    WORD_LENGTH: int
        - The length of the word that the players have to change.

    START_CARDS_AMOUNT: int
        - How many cards each player starts with.

    WORDS_FILE_NAME: str
        - The name of the file that contains the data for the words.

    WORD_FREQUENCIES: dict[str, int]
        - All words & their relative frequencies in % (i.e. how common they are in the English language).

    WORDS: set[str]
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
        self.TURN_TIME_LIMIT = 15 # the maximum amount of time a player can take to play their turn
        self.MAX_CARDS = 15 # the amount of cards that if you exceed, you lose the game
        self.WORD_LENGTH = 3 # the length of the word that the players have to change
        self.START_CARDS_AMOUNT = 7 # how many cards each player starts with
        self.WORDS_FILE_NAME = "data/word_frequencies_json.txt"  # name of the file that contains the data for the words
        # dictionary for all words & their relative frequencies in % (i.e. how common they are in the English language)
        self.WORD_FREQUENCIES = self.load_word_frequencies()
        # all real words that can be played in the game (all are of the length specified in self.word_length)
        self.WORDS = self.get_words()

    def load_word_frequencies(self) -> dict[str, int]:
        """Return a dictionary of all words and their frequencies from the words file (i.e. self.words_file_name)."""
        try: # attempt the following code
            with open(self.WORDS_FILE_NAME, "r") as file: # opens the words file in read mode (& closes it when done)
                word_frequencies = json.loads(file.readline()) # loads the file from json format to a python dictionary
                return word_frequencies
        except FileNotFoundError: # checks for the error that happens when the program can't find the file
            raise FileNotFoundError(f"\nThe file {self.WORDS_FILE_NAME} was not found. " # stop program & display error
                                    f"Please make sure all game files are downloaded and in the correct folder.")

    def get_words(self) -> set[str]:
        """Return all the words that are allowed to be played in the game as a set."""
        # from the words in the word_frequency dictionary, filter out all words that are not of the specified length
        # using a set for faster lookup
        words = set((filter(lambda word: len(word) == self.WORD_LENGTH, self.WORD_FREQUENCIES.keys())))
        return words


game_settings = GameSettings() # initiate class object (to be called by other modules)