import random
from collections import deque

#function class game created by Raghad
class Game:
    def __init__(self):
        self.words = self.load_letter_words("words_alpha.txt")

    # Loading the words from a file
    def load_letter_words(self, filename):
        try:
            with open(filename, 'r') as file:
                words = {line.strip().lower() for line in file.readlines()}  # Using a set for faster lookup
            return words
        except FileNotFoundError:
            print("File not found.")
            return set()

    # Check if two words differ by exactly one letter
    def just_one_letter_diff(self, word1, word2):
        diff_count = sum(1 for a, b in zip(word1, word2) if a != b)
        return diff_count == 1

    # Generate all valid transformations using BFS
    def get_valid_transformations(self, start_word):
        queue = deque([start_word])  #  the start word
        visited = set([start_word])  # Keep track of visited words
        valid_transformations = []

        while queue:
            word = queue.popleft()

            # Check all possible neighbors (one letter change)
            for candidate in self.words:
                if candidate not in visited and self.is_one_letter_diff(word, candidate):
                    valid_transformations.append(candidate)
                    visited.add(candidate)
                    queue.append(candidate)

        return valid_transformations


    #Random letter shuffling generator
    def shuffling_letter(self):
        letters = [chr(i) for i in range(65, 91)]  # Generates letters from A to z
        n = len(letters)
        for i in range(n - 1, 0, -1):  # Shuffle Algorithm  (Fisher-Yates)
            j = random.randint(0, i)
            letters[i], letters[j] = letters[j], letters[i]
        return letters  # Returns the shuffled letters

    #Function star card (random u might or might not get one)
    def star_card(self):
        value=random.randint(0, 2)
        if value == 0:
            print("Head")
        else:
            print("Tail")

    # it will return a list of 10 cards
    def cards(self):
        print("it will call the 2 function above")


    #soriting palyer cards in assending order
    def sorting_cards(self,unsorted_list):
        print("NOTHING")

    # generate a three letter or four word
    def word_generater(self):
        print("NOTHING")

    #return true or false if the pesron onlu changed one letter it can be romoved by interface
    def changed_one(self,prevuos,after):
        print("NOTHING")
    # chek if the  the word has been changed is it real or not
    def check_exists(self):
        print("NOTHING")
    #decide wich palyer start fisrt
    def coin(self):
        print("NOTHING")



#test
a=Game()








