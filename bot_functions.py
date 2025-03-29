#functions for the bot player, by Hasan Alwazzan (5640356)
import random
import time

class Bot:
    '''
    [insert docstring]
    '''

    def __init__(self, difficulty_level="medium", cards=[]):
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

    def play_turn(self):
        ...
    def find_next_answer(self):
        ...
    def discard_card(self):
        ...
    def draw_card(self):
        ...
    def answer_or_not(self):
        ...
    def answer_time(self):
        average_answer_time = self.difficulty_settings[self.difficulty_level]["average_answer_time"]
        variance_answer_time = self.difficulty_settings[self.difficulty_level]["variance_answer_time"]
        answer_time = random.normalvariate(average_answer_time, variance_answer_time)
        if answer_time <= 0:
            return 0
        if answer_time >= 15:
            return 15
        else:
            return answer_time