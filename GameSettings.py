"""
General variables for the game settings to be used by other files.
"""
# Developed by Hasan Alwazzan (5640356).


# Importing library.
import json


class GameSettings:
    """
    A class that stores the game settings as variables.

    Attributes
    ----------
    TURN_TIME_LIMIT: int
        - The maximum amount of time a player can take
            to play their turn.

    MAX_CARDS: int
        - The amount of cards that if you exceed, you lose the game.

    WORD_LENGTH: int
        - The length of the word that the players have to change.

    START_CARDS_AMOUNT: int
        - How many cards each player starts with.

    BOT_WORDS_FILE_NAME: str
        - The name of the file that contains the data
            for word frequencies and the bot's words

    WORD_FREQUENCIES: dict[str, int]
        - Words and their relative frequencies in %
            (i.e. how common they are in the English language).

    ALL_BOT_WORDS: set[str]
        - All the words that the bot can play.All are of the length
            specified by self.word_length (e.g. 3 letters long)

    Methods
    -------
    load_word_frequencies():
        - Return a dictionary of all words and their frequencies
            from the bot's words file (self.words_file_name).

    get_all_bot_words():
        - Return a set of all the words that the bot is allowed to play.
    """

    def __init__(self):
        """
        Construct all the necessary attributes for
            the GameSettings object.
        """
        self.TURN_TIME_LIMIT = 15  # The maximum amount of time a player can take to play their turn.
        self.MAX_CARDS = 15  # The amount of cards that if you exceed, you lose the game.
        self.WORD_LENGTH = 3  # The length of the word that the players have to change.
        self.START_CARDS_AMOUNT = 7  # How many cards each player starts with.

        # The name of the file that contains the data for word frequencies and the bot's words.
        self.BOT_WORDS_FILE_NAME = "data/word_frequencies_json.txt"
        # Dictionary for words & their relative frequencies in % (i.e. how common they are in the English language).
        self.WORD_FREQUENCIES = self.load_word_frequencies()
        # The set of all words the bot can use (all are of the length specified by word_length e.g. 3 letters long).
        self.ALL_BOT_WORDS = self.get_all_bot_words()

    def load_word_frequencies(self) -> dict[str, int]:
        """
        Return a dictionary of all words and their frequencies
            from the bot's words file (self.BOT_WORDS_FILE_NAME).
        """
        try:  # Attempt the following code.
            with open(self.BOT_WORDS_FILE_NAME, "r") as file:  # Open the words file in read mode & closes it when done.
                word_frequencies = json.loads(file.readline())  # Load the file from json format to a python dictionary.
                return word_frequencies
        except FileNotFoundError:  # Checks for the error that happens when the program can't find the file.
            # Stop program & show error.
            raise FileNotFoundError(f"\nThe file {self.BOT_WORDS_FILE_NAME} was not found. "
                                    f"Please make sure all game files are downloaded and are in the correct folder.")

    def get_all_bot_words(self) -> set[str]:
        """
        Return a set of all the words that the bot is allowed to play.
        """
        # From the words in the word frequency dictionary, filter out all words that are not of the specified length.
        # Using a set for faster lookup.
        words = set((filter(lambda word: len(word) == self.WORD_LENGTH, self.WORD_FREQUENCIES.keys())))
        return words