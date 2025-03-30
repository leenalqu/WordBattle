#functions for the bot player, by Hasan Alwazzan (5640356)
import random
import time

class Bot:
    '''
    [insert docstring]
    '''

    def __init__(self, difficulty_level="medium", cards=[]): # initiated with default values to avoid errors
        self.difficulty_level = difficulty_level # chosen difficulty setting of the bot
        self.cards = cards # list of the bots set of cards
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
        self.letter_distribution = { # dictionary to store all how often each letter is used
            "a": float("inf"), "b": float("inf"), "c": float("inf"), "d": float("inf"), "e": float("inf"), "f": float("inf"), "g": float("inf"),
            "h": float("inf"), "i": float("inf"), "j": float("inf"), "k": float("inf"), "l": float("inf"), "m": float("inf"), "n": float("inf"),
            "o": float("inf"), "p": float("inf"), "q": 1, "r": float("inf"), "s": float("inf"), "t" : float("inf"), "u" : float("inf"),
            "v": float("inf"), "w": float("inf"), "x": 0.5, "y": float("inf"), "z": 0
        } # NOTE: CURRENT DICTIONARY IS NOT CORRECT, JUST A TEST

    def play_turn(self, current_word, card_stack, discard=False):
        ...
    def find_next_answer(self):
        ...
    def discard_card(self): # MIGHT CHANGE BASED ON IMPLEMENTATION
        worst_card = self.cards[0]
        for letter in self.cards:
            if self.letter_distribution[letter] < self.letter_distribution[worst_card]:
                worst_card = letter
        self.cards.remove(worst_card)

    def draw_card(self, card_stack): # IMPORT STACK
        top_card = card_stack.pop()
        self.cards.append(top_card)

    def answer_or_not(self):
        answer_probability = (
            self.difficulty_settings)[self.difficulty_level]["answer_probability"] # gets the answer probability from settings based on the difficulty
        random_probability = random.random() # gets random number between 0 and 1
        if random_probability < answer_probability: # check if the random number is between 0 and the set answer probability
            return True
        else:
            return False

    def answer_time(self): # function that returns how long the bot will take to play its turn
        average_answer_time = (
            self.difficulty_settings)[self.difficulty_level]["average_answer_time"] # gets the average answer time based on the chosen difficulty
        variance_answer_time = self.difficulty_settings[self.difficulty_level]["variance_answer_time"] # gets the variance based on the chosen difficulty
        answer_time = random.normalvariate(average_answer_time, variance_answer_time) # randomly setting the answer time based on a normal distribution
        if answer_time <= 0: # avoiding negative values for answer_time
            return 0
        if answer_time >= 15: #avoiding answer_time going over the time limit
            return 15
        else:
            return answer_time