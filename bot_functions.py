# functions for the bot player, by Hasan Alwazzan (5640356)

#importing libraries and modules
import random
from GameFunctions import Game # MIGHT CHANGE BASED ON GAMEFUNCTIONS CODE ALSO MIGHT CHANGE CUS OF INNITIALIZATION ISSUE

class Bot:
    """
    A Bot that plays the card game against the player.

    Attributes
    ----------
    difficulty_level: str
        - How difficult the bot is
    cards: list[str]
        - The cards that the bot can play
    difficulty_settings: dict[str, dict[str, int]]
        - Settings that specify variables for each difficulty level
    letter_distribution: dict[str, int]
        - Dictionary for the relative frequencies of letters (%)
    ran_current_turn_code: bool
        - Whether the initial code of the current turn has run
    current_turn_answer_or_not: bool
        - Whether the bot will answer in the current turn
    current_turn_answer_time: int
        - How long the bot will take to answer the current turn
    current_turn_answer: int
        - The bots answer in the current turn

    Methods
    -------
    play_turn(current_word, current_timer):
        - Handle the bots turn in the game loop
    next_word(current_word, words):
        - Return the bots answer
    letter_distribution_sort(cards_list):
        - Sort the cards based on letter distribution
    discard_card():
        - Discard the worst card from the bot
    draw_card(card_stack):
        - Draw a card from the deck
    answer_or_not():
        - Decide whether the bot will play that turn or not
    answer_time():
        - Return how long the bot will take to play its turn (seconds)
    """

    # initiation with default values to avoid errors
    def __init__(self, difficulty_level: str = "medium", cards: list[str] = None):
        """
        Construct all the necessary attributes for the bot object.

        Parameters
        ----------
        difficulty_level: str
            - How difficult the bot is
        cards: list[str]
            - The cards that the bot can play
        """
        self.difficulty_level = difficulty_level # chosen difficulty setting of the bot
        if cards is None: self.cards = []  # if no cards list is given set cards to empty list
        self.ran_current_turn_code = False  # whether the initial code of the turn has run
        self.current_turn_answer_or_not = False  # whether the bot will answer this turn
        self.current_turn_answer_time = 0  # how long the bot will take to answer this turn
        self.current_turn_answer = 0  # the bots answer in this turn
        self.difficulty_settings = { # dictionary for the settings based on the chosen difficulty mode
            "easy": { # difficulty mode
                "answer_probability": 0.6, # determines how often the bot plays and doesn't run down the time
                "average_answer_time": 6, # mean answer time
                "variance_answer_time": 1.5 # determines how varies the answer times are
            },
            "medium": {
                "answer_probability": 0.75,
                "average_answer_time": 4,
                "variance_answer_time": 1.5
            },
            "hard": {
                "answer_probability": 0.9,
                "average_answer_time": 2,
                "variance_answer_time": 1.5
            },
        }
        self.letter_distribution = { # dictionary to store all how often each letter is used (%)
            "a": 8.12, "b": 1.49, "c": 2.71, "d": 4.32, "e": 12.02,
            "f": 2.30, "g": 2.03, "h": 5.92, "i": 7.31, "j": 0.10,
            "k": 0.69, "l": 3.98, "m": 2.61, "n": 6.95, "o": 7.68,
            "p": 1.82, "q": 0.11, "r": 6.02, "s": 6.28, "t": 9.10,
            "u": 2.88, "v": 1.11, "w": 2.09, "x": 0.17, "y": 2.11,
            "z": 0.07
        }

    def play_turn(self, current_word: str, current_timer: int) -> str: # function to handle the bots turn in the game loop
        if not self.ran_current_turn_code: # makes sure the code in this statement only runs once in a turn
            self.current_turn_answer_or_not = self.answer_or_not() # whether the bot will answer this turn
            self.current_turn_answer_time = self.answer_time() # how long the bot will take to answer this turn
            self.current_turn_answer = self.next_word(current_word) # the bots answer in this turn
            self.ran_current_turn_code = True # NEEDS TO BE SET BACK TO FALSE # tells program that this code has run in this turn
        elif not self.current_turn_answer_or_not: # if the bot won't answer this turn
            return "thinking" # program will keep returning "thinking" until the bots turn ends
        elif 15 - current_timer >= self.current_turn_answer_time: # MIGHT CHANGE HARDCODE 15 # when timer reaches the time set by the bot to answer
            return self.current_turn_answer # returns the bots answer
        else:
            return "thinking" # when the timer hasn't reached the set amount, return "thinking"

    def next_word(self, current_word: str, words: set[str] = None) -> str: # Game().words -> NAME MIGHT CHANGE # function to find the bots answer
        if words is None: # if no words argument has been specified
            words = Game().words # sets words variable to the set of all english words
        neighbor_suggestions = [] # list for suggestions (neighbor meaning a word with 1 letter changed from the current word)
        cards_list = self.cards # the bots cards
        if self.difficulty_level == "hard": # if the bot is in hard mode
            # sort cards by least frequency to use hard cards first
            cards_list = self.letter_distribution_sort(cards_list)

        for letter in cards_list: # loops through the bots cards
            for j in range(len(current_word)): # loops the amount of letters in the current word
                new_word = list(current_word) # list of characters of the current word
                new_word[j] = letter # replace the letters of the current word to create a new word
                new_word = "".join(new_word) # join back the list into a string
                #condition: make sure the word is a real word, and it is not the current word, and not one of the suggestions
                if new_word in words and new_word != current_word and new_word not in neighbor_suggestions:
                    neighbor_suggestions.append(new_word) # add to suggestions list
                    break # stop looking for words using this card (only takes the first suggestion)

        if not neighbor_suggestions: #if no suggestions are found (meaning if the neighbor_suggestions list has items)
            return "word not found" # MIGHT CHANGE
        elif self.difficulty_level == "hard": # when the bot is in hard mode
            return neighbor_suggestions[0] # uses first suggestion (because it is the one that uses the hardest card)
        else: # easy and medium modes
            random_index = random.randint(0, len(neighbor_suggestions) - 1) # random suggestion index
            return neighbor_suggestions[random_index] # return suggestion

    # insertion sort to sort the cards based on letter distribution
    def letter_distribution_sort(self, cards_list: list[str]) -> list[str]:
        for i in range(1, len(cards_list)): # loops from the 2nd position to the end
            key = cards_list[i] # current letter that is being inserted into position
            j = i - 1 # previous index

            # loop to find position of the current letter
            while j >= 0 and self.letter_distribution[key] < self.letter_distribution[cards_list[j]]: # compare letter distributions
                cards_list[j + 1] = cards_list[j] # move card at index j forward
                j -= 1 # move j index back
            cards_list[j + 1] = key # insert card in correct position
        return cards_list

    def discard_card(self) -> None: # MAYBE CHANGE THIS # function that discard the worst card from the bot (in discard case)
        worst_card = self.cards[0] # initiate variable for the worst card as the bots first card
        for letter in self.cards: # loops through the bots cards
            if self.letter_distribution[letter] < self.letter_distribution[worst_card]: # checks if the current letter is less common
                worst_card = letter # sets the current letter as the worst
        self.cards.remove(worst_card) # remove the worst ccard from bots cards

    def draw_card(self, card_stack: list[str]) -> None: # CARD STACK IS NOT IMPLEMENTED YET # function to draw a card from the deck
        top_card = card_stack.pop() # FUCNTION MIGHT BE WRONG # take top card
        self.cards.append(top_card) # add to bots list of cards

    def answer_or_not(self) -> bool: # function to decide if the bot will play that turn or not
        # gets the answer probability from settings based on the difficulty
        answer_probability = (self.difficulty_settings)[self.difficulty_level]["answer_probability"]
        random_probability = random.random() # gets random number between 0 and 1
        if random_probability < answer_probability: # check if the random number is between 0 and the set answer probability
            return True
        else:
            return False

    def answer_time(self) -> int: # function that returns how long the bot will take to play its turn
        # gets the average answer time based on the chosen difficulty
        average_answer_time = self.difficulty_settings[self.difficulty_level]["average_answer_time"]
        # gets the variance based on the chosen difficulty
        variance_answer_time = self.difficulty_settings[self.difficulty_level]["variance_answer_time"]
        # randomly setting the answer time based on a normal distribution
        answer_time = random.normalvariate(average_answer_time, variance_answer_time)
        if answer_time <= 0: # avoiding negative values for answer_time
            return 0
        if answer_time >= 15 - 1: # avoiding answer_time going over the time limit (subtracting 1 to give leeway to answer)
            return 15 - 1 # MIGHT CHANGE CUZ HARD CODING 15
        else:
            return answer_time

#testing
if __name__ == "__main__":
    b = Bot()
    from CardGameUI import game
    print(game.timer_duration - game.timer_seconds >= b.current_turn_answer_time)