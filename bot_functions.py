#functions for the bot player, by Hasan Alwazzan (5640356)

#importing libraries and modules
import time
import random
from GameFunctions import Game # MIGHT CHANGE BASED ON GAMEFUNCTIONS CODE

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
        self.letter_distribution = { # dictionary to store all how often each letter is used (%)
            "a": 8.12, "b": 1.49, "c": 2.71, "d": 4.32, "e": 12.02,
            "f": 2.30, "g": 2.03, "h": 5.92, "i": 7.31, "j": 0.10,
            "k": 0.69, "l": 3.98, "m": 2.61, "n": 6.95, "o": 7.68,
            "p": 1.82, "q": 0.11, "r": 6.02, "s": 6.28, "t": 9.10,
            "u": 2.88, "v": 1.11, "w": 2.09, "x": 0.17, "y": 2.11,
            "z": 0.07
        }

    def play_turn(self, current_word, card_stack, discard=False):
        ...

    def next_word(self, current_word, words=Game().words): # .words -> NAME MIGHT CHANGE
        neighbor_suggestions = []
        cards_list = self.cards
        if self.difficulty_level == "hard":
            cards_list = self.letter_distribution_sort(cards_list) # MIGHT CHANGE

        for i in cards_list:
            for j in range(len(current_word)):
                new_word = list(current_word)
                new_word[j] = i
                new_word = "".join(new_word)
                if new_word in words and new_word != current_word and new_word not in neighbor_suggestions:
                    neighbor_suggestions.append(new_word)
                    break

        if not neighbor_suggestions: #if no suggestions are found (meaning if the neighbor_suggestions list has items)
            return None # MIGHT CHANGE
        elif self.difficulty_level == "hard":
            return neighbor_suggestions[0]
        else:
            random_index = random.randint(0, len(neighbor_suggestions) - 1)
            return neighbor_suggestions[random_index]

    def letter_distribution_sort(self, cards_list): # insertion sort to sort the cards based on letter distribution
        for i in range(1, len(cards_list)): # loops from the 2nd position to the end
            key = cards_list[i] # current letter that is being inserted into position
            j = i - 1 # previous index

            # loop to find position of the current letter
            while j >= 0 and self.letter_distribution[key] < self.letter_distribution[cards_list[j]]: # compare letter distributions
                cards_list[j + 1] = cards_list[j] # move card at index j forward
                j -= 1 # move j index back
            cards_list[j + 1] = key # insert card in correct position
        return cards_list

    def discard_card(self): # MIGHT CHANGE BASED ON IMPLEMENTATION
        worst_card = self.cards[0]
        for letter in self.cards:
            if self.letter_distribution[letter] < self.letter_distribution[worst_card]:
                worst_card = letter
        self.cards.remove(worst_card)

    def draw_card(self, card_stack): # CARD STACK IS NOT IMPLEMENTED YET
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

#testing
if __name__ == "__main__":
    t1 = time.time()
    b = Bot("hard", ['a', 'b', 'z'])
    c = b.next_word("pop")
    t2 = time.time()
    print(c)
    print(t2-t1)