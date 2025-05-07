# functions for the bot player, by Hasan Alwazzan (5640356)

#importing libraries and modules
import random
from GameSettings import GameSettings
from enum import Enum


class Bot:
    """
    A Bot that plays the card game against the player.

    Attributes
    ----------
    difficulty_level: Difficulty
        - How difficult the bot is.
        - Must be either Bot.Difficulty.EASY or
         Bot.Difficulty.MEDIUM or Bot.Difficulty.HARD.

    cards: list[str]
        - The cards that the bot can play.

    ran_current_turn_code: bool
        - Whether the initial code of the current turn has run.

    current_turn_will_answer_or_not: bool
        - Whether the bot will answer in the current turn.

    current_turn_answer_time: float
        - How long the bot will take to answer the current turn.

    current_turn_answer: str
        - The bots answer in the current turn.

    difficulty_settings: dict[str, dict[str, int]]
        - Settings that specify variables for each difficulty level.

    letter_frequencies: dict[str, int]
        - Dictionary for the relative frequencies of letters (%).

    bot_words: set[str]
        - Set of all the words the bot can use.

    Methods
    -------
    play_turn(current_word, current_timer):
        - Return the bots answer or Bot.Output.THINKING if the bot
        is not ready to answer or if it won't answer at all.

    end_turn():
        - End the bots turn.

    next_word(current_word):
        - Return the bots answer.

    letter_frequency_sort(cards_list):
        - Sort the cards based on letter distribution.

    discard_card():
        - Discard the worst card from the bot.

    draw_card(card_deck):
        - Draw a card from the deck.

    will_answer_or_not():
        - Decide whether the bot will play that turn or not.

    answer_time():
        - Return how long the bot will take to play its turn (seconds).

    get_bot_words()
        - Initialize the set of words that the bot can
        use to find a new word.

    add_card(letter):
        - Add a card to the bots cards.

    remove_cards(letter):
        - Remove a card from the bots cards.

    won_game():
        - Return whether the bot has won the game.
    """

    class Difficulty(Enum):
        EASY: str = "easy"
        MEDIUM: str = "medium"
        HARD: str = "hard"

    class Output(Enum):
        THINKING: str = "thinking"

    game_settings = GameSettings()  # initiate game settings object to stores game settings constants

    def __init__(self, difficulty_level: Difficulty, cards: list[str] = None):
        """
        Construct all the necessary attributes for the bot object.

        Parameters
        ----------
        difficulty_level: Difficulty
            - How difficult the bot is.
            - Must be either Bot.Difficulty.EASY or Bot.Difficulty.MEDIUM or Bot.Difficulty.HARD.

        cards: list[str]
            - The cards that the bot can play.
        """
        # how difficult the bot is (must be one of Bot.Difficulty.EASY or Bot.Difficulty.MEDIUM or Bot.Difficulty.HARD)
        self.difficulty_level = difficulty_level
        if cards is None: cards = []  # if no cards list is given set cards to empty list
        self.cards = cards  # the letter cards the bot can use

        self.ran_current_turn_code = False  # initial variable for whether the initial code of the turn has run
        self.current_turn_will_answer_or_not = False  # initial variable for whether the bot will answer this turn
        self.current_turn_answer_time = 0  # initial variable for how long the bot will take to answer this turn
        self.current_turn_answer = ""  # initial variable for the bots answer in this turn
        self.current_turn_card_used = "" # initial variable for the card the bot will play in this turn

        self.difficulty_settings = {  # dictionary for the settings based on the chosen difficulty mode
            Bot.Difficulty.EASY: {  # difficulty mode
                "ANSWER_PROBABILITY": 0.95,  # determines how often the bot plays its turn (doesn't run down the timer)
                "AVERAGE_ANSWER_TIME": 0.566 * Bot.game_settings.TURN_TIME_LIMIT,  # mean answer time
                "VARIANCE_ANSWER_TIME": 0.133 * Bot.game_settings.TURN_TIME_LIMIT,  # how varied the answer times are
                # determines the cut-off that determines which words are included in the bots dictionary of words
                "WORD_FREQUENCY_CUTOFF": 5.752713813881526e-06  # (word frequency means how common the word is)
            },
            Bot.Difficulty.MEDIUM: {
                "ANSWER_PROBABILITY": 0.95,
                "AVERAGE_ANSWER_TIME": 0.466 * Bot.game_settings.TURN_TIME_LIMIT,
                "VARIANCE_ANSWER_TIME": 0.133 * Bot.game_settings.TURN_TIME_LIMIT,
                "WORD_FREQUENCY_CUTOFF": 2.9838168355859476e-06
            },
            Bot.Difficulty.HARD: {
                "ANSWER_PROBABILITY": 0.9,
                "AVERAGE_ANSWER_TIME": 0.366 * Bot.game_settings.TURN_TIME_LIMIT,
                "VARIANCE_ANSWER_TIME": 0.133 * Bot.game_settings.TURN_TIME_LIMIT,
                "WORD_FREQUENCY_CUTOFF": 0  # the hard bot doesn't have a cut-off and can use all words
            }
        }
        self.letter_frequencies = {  # dictionary to store all how often each letter is used (%)
            "a": 8.12, "b": 1.49, "c": 2.71, "d": 4.32, "e": 12.02,
            "f": 2.30, "g": 2.03, "h": 5.92, "i": 7.31, "j": 0.10,
            "k": 0.69, "l": 3.98, "m": 2.61, "n": 6.95, "o": 7.68,
            "p": 1.82, "q": 0.11, "r": 6.02, "s": 6.28, "t": 9.10,
            "u": 2.88, "v": 1.11, "w": 2.09, "x": 0.17, "y": 2.11,
            "z": 0.07
        }
        self.bot_words = self.get_bot_words()  # set of all the words the bot can use

    def play_turn(self, current_word: str, current_timer: int) -> tuple | Output:
        """
        Handle the bots turn in the game loop.
        Return the bots answer or Bot.Output.THINKING if the bot is not ready to answer or if it won't answer at all.

        Parameters
        ----------
        current_word: str
            - The current word in the game that the bot must change.

       current_timer: int
            - How much time has passed since the start of the bots turn.
        """
        # initial code for the turn (which runs once per turn)
        current_word = current_word.lower() # converts current word to lowercase (bot only works with lowercase)
        if not self.ran_current_turn_code:  # makes sure the code in this statement only runs once in a turn
            self.current_turn_will_answer_or_not = self.will_answer_or_not()  # whether the bot will answer this turn
            self.current_turn_answer_time = self.answer_time()  # how long the bot will take to answer this turn
            # the bots answer in this turn and the card used to get that answer
            self.current_turn_answer, self.current_turn_card_used = self.next_word(current_word)
            self.ran_current_turn_code = True  # tells program that this code has run in this turn

        # output manager for the loop
        if not self.current_turn_will_answer_or_not:  # if the bot won't answer this turn
            return Bot.Output.THINKING  # program will keep returning Bot.Output.THINKING until the bots turn ends
        elif not (Bot.game_settings.TURN_TIME_LIMIT - current_timer) >= self.current_turn_answer_time:
            return Bot.Output.THINKING  # when the timer hasn't reached the set time, return Bot.Output.THINKING
        # when timer reaches the time set by the bot to answer
        elif self.current_turn_answer is None:  # if the bot didn't find an answer
            return Bot.Output.THINKING
        else:  # when the bot has an answer and the timer is has reached the set time
            return self.current_turn_answer, self.current_turn_card_used  # returns the bots answer and the card it used

    def end_turn(self) -> None:
        """
        End the bots turn.
        """
        self.ran_current_turn_code = False

    def next_word(self, current_word: str) -> tuple:
        """
        Return the bots answer as a string (if no word is found Return None).

        Parameters
        ----------
        current_word: str
            - The current word in the game that the bot must change.
        """
        # declaring variables
        alphabet = self.letter_frequencies.keys() # all english letters (from keys of letter_frequencies dictionary)
        star_card = "*" # variable to define the star card
        star_card_word = "" # initialize a variable for the answer that uses the star card
        neighbor_suggestions = []  # word suggestions (neighbor is a word with 1 letter changed from the current word)
        cards_list = self.cards  # the bots cards
        if self.difficulty_level == Bot.Difficulty.HARD:  # if the bot is in hard mode
            cards_list = self.letter_frequency_sort(cards_list) # sort cards by least frequency to use hard cards first

        # getting neighbor suggestions
        for card in cards_list:  # loops through the bots cards
            if card in alphabet: # make sure card is a letter (avoid any special cards)
                for j in range(len(current_word)):  # loops the amount of letters in the current word
                    # swapping 1 letter from the word
                    characters = list(current_word)  # list of characters of the current word
                    characters[j] = card  # replace one of the letters of the current word to create a new word
                    new_word = "".join(characters)  # join back the list into a string
                    # make sure the word is a real word, & it is not the current word, & not one of the suggestions
                    if new_word in self.bot_words and new_word != current_word and new_word not in neighbor_suggestions:
                        # add suggestion to list with the card used to get it
                        neighbor_suggestions.append((new_word, card))
                        break # stop looking for words using this card (only takes the first suggestion)
            elif card == star_card: # if the current card is a star card
                for letter in alphabet: # loop through all english letters
                    for k in range(len(current_word)):  # loops the amount of letters in the current word
                        # swapping 1 letter from the word
                        characters = list(current_word)  # list of characters of the current word
                        characters[k] = letter  # replace one of the letters of the current word to create a new word
                        new_word = "".join(characters)  # join back the list into a string
                        # make sure the word is a real word, & it is not the current word, & not one of the suggestions
                        if new_word in self.bot_words and new_word != current_word:
                            characters = list(new_word)  # list of characters of the new word
                            characters[k] = star_card # replace the changed letter with the star card
                            star_card_word = "".join(characters)  # join back the list into a string
                            break
            else:
                # stop the program if an unknown card is found (edge case)
                raise Exception("\nError: Unknown card was found in Bot's card list")

        # selecting the next word from neighbor suggestions
        if neighbor_suggestions:  # suggestions are found (meaning if the neighbor_suggestions list is not empty)
            match self.difficulty_level: # check difficulty level of the bot, and run the code that matches it
                case Bot.Difficulty.EASY | Bot.Difficulty.MEDIUM:  # if bot in easy or medium modes
                    random_index = random.randint(0, len(neighbor_suggestions) - 1)  # get random suggestion index
                    next_word = neighbor_suggestions[random_index]  # choose random suggestion
                    return next_word
                case Bot.Difficulty.HARD:  # when the bot is in hard mode
                    # uses first suggestion because it's the one that uses the hardest card
                    next_word = neighbor_suggestions[0]
                    return next_word
                case _:
                    raise Exception("\nError: Unknown difficulty mode was set for Bot")
        # in the case that that bot doesn't find any normal answers
        elif star_card_word: # check whether an answer using the star card has been found
            return star_card_word, star_card
        else:
            return None, None

    def letter_frequency_sort(self, cards_list: list[str]) -> list[str]:  # variation of insertion sort
        """
        Sort cards based on the letter frequency distribution
        in the English language, and any Special cards (e.g. Star cards)
        are placed at the end of the sorted list.

        Parameters
        ----------
        cards_list: list[str]
            - List of cards (letters and special cards).
        """
        letter_cards, special_cards = [], []  # initiate empty lists to separate the letter cards from special ones
        alphabet = self.letter_frequencies.keys() # all english letters (from keys of letter_frequencies dictionary)
        for card in cards_list:  # loop through cards
            if card in alphabet: # if a card is a letter
                letter_cards.append(card)  # add it to the letter cards list
            else: # otherwise
                special_cards.append(card)  # add it to the special cards list

        #sort the letter cards using insertion sort
        for i in range(1, len(letter_cards)):  # loops from the 2nd position to the end
            key = letter_cards[i]  # current letter that is being inserted into position
            j = i - 1  # previous index
            # loop to find position of the current letter (by comparing letter frequencies)
            while j >= 0 and self.letter_frequencies[key] < self.letter_frequencies[letter_cards[j]]:
                letter_cards[j + 1] = letter_cards[j]  # move card at index j forward
                j -= 1  # move j index back
            letter_cards[j + 1] = key  # insert card in correct position

        sorted_cards_list = letter_cards + special_cards  # join the two lists into one list after sorting the letters
        return sorted_cards_list

    def discard_card(self) -> None:
        """
        Discard a card from the bot.
        """
        alphabet = self.letter_frequencies.keys() # all english letters (from keys of letter_frequencies dictionary)

        if self.difficulty_level == Bot.Difficulty.EASY:  # when the bot is in easy mode
            card_to_remove_index = random.randint(0, len(self.cards) - 1)  # pick a random index from the cards list
            self.cards.pop(card_to_remove_index)  # remove the card from the bots cards

        elif self.difficulty_level in (Bot.Difficulty.MEDIUM, Bot.Difficulty.HARD):  # if bot is in medium or hard mode
            worst_card = self.cards[0]  # initiate variable for the worst card as the bots first card
            for card in self.cards:  # loops through the bots cards
                try: # tries the following code
                    # checks if the current letter is less common
                    if self.letter_frequencies[card] < self.letter_frequencies[worst_card]:
                        worst_card = card  # sets the current letter as the worst
                except KeyError:
                    # Runs when the frequency of the star card is checked
                    # (which returns an error because it is not in the letter_frequencies dictionary)
                    if worst_card not in alphabet: # if the initial worst card is a special card
                        worst_card = card # Set the worst card to the current card.
                    else: # This case means the current card is a special card.
                        continue  # Skip the special card and continue the loop.

            self.cards.remove(worst_card)  # remove the worst card from bots cards

        else: # This case means the bot difficulty level wasn't found.
            raise Exception("\nError: Unknown difficulty mode was set for Bot")

    def will_answer_or_not(self) -> bool:
        """
        Decide if the bot will play that turn or not.
        Return True or False.

        (True means that the bot will play its turn,
        and False means that it will not).
        """
        # gets the answer probability from settings based on the difficulty
        answer_probability = self.difficulty_settings[self.difficulty_level]["ANSWER_PROBABILITY"]
        random_probability = random.random()  # gets random number between 0 and 1
        # check if the random number is within the range of the answer probability (i.e. between 0 & the probability)
        if random_probability < answer_probability:
            return True
        else:
            return False

    def answer_time(self) -> float:
        """
        Return how long the bot will take to play its turn.
        """
        # gets the average answer time based on the chosen difficulty
        average_answer_time = self.difficulty_settings[self.difficulty_level]["AVERAGE_ANSWER_TIME"]
        # gets the variance based on the chosen difficulty
        variance_answer_time = self.difficulty_settings[self.difficulty_level]["VARIANCE_ANSWER_TIME"]
        # randomly setting the answer time based on a normal distribution
        answer_time = random.normalvariate(average_answer_time, variance_answer_time)
        if answer_time <= 3:  # avoiding bot from answering too fast
            return 3
        # avoiding answer_time going over the time limit (subtracting 1 to give leeway to answer)
        elif answer_time >= Bot.game_settings.TURN_TIME_LIMIT - 1:
            return Bot.game_settings.TURN_TIME_LIMIT - 1
        else:
            return answer_time

    def get_bot_words(self) -> set[str]:
        """
        Return the set of words that the bot can use to find a new word.
        """
        word_frequencies = Bot.game_settings.WORD_FREQUENCIES  # dictionary of words and how common they are
        all_bot_words = Bot.game_settings.ALL_BOT_WORDS  # all the words that can be played in the game
        # cut-off that determines which words are included in the bots dictionary of words
        frequency_cutoff = self.difficulty_settings[self.difficulty_level]["WORD_FREQUENCY_CUTOFF"]

        # filter function to remove words that are uncommon (under the frequency cutoff) based on the difficulty setting
        bot_words = set((filter(lambda word: word_frequencies[word] > frequency_cutoff, all_bot_words)))
        return bot_words

    def add_card(self, letter: str) -> None:
        """
        Add a card to the bots cards.

        Parameters
        ----------
        letter: str
            - The letter of the card.
        """
        self.cards.append(letter.lower()) # add card to bots card list

    def remove_cards(self, letter: str) -> None:
        """
        Remove a card from the bots cards.

        Parameters
        ----------
        letter: str
            - The letter of the card.
        """
        if letter.lower() in self.cards: # makes sure the letter is in the cards list
            self.cards.remove(letter.lower()) # remove the card

    def won_game(self) -> bool:
        """
        Return whether the bot has won the game.
        """
        return len(self.cards) == 0 # the winner is announced when they finish all their cards

#testing
if __name__ == "__main__":
    b = Bot(Bot.Difficulty.MEDIUM, ['a', '*', 'e','f','i','k','r','o'])
    b.discard_card()
    out = b.cards
    print(out)
    ...