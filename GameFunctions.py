import random
from collections import deque
# 1 function class game created by Raghad

# class functions
class Game:
    def __init__(self):
        self.words = self.load_letter_words("words_alpha.txt")
        # Filter out only the three-letter words
        self.words = self.words = {word for word in self.words if len(word) == 3}

    # Loading the words from a file
    def load_letter_words(self, filename):
        try:
            with open(filename, 'r') as file:
                words = {line.strip().lower() for line in file.readlines()}  # Using a set for faster lookup
            return words
        except FileNotFoundError:
            print("File not found.")
            return set()

    # Generate all valid transformations using BFS    (not finshed)
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

    #Function star card (random u might or might not get one if you dont get a star card you will be given a random letter)
    def star_card(self):
        value = random.randint(0, 2)
        if value == 0:
            return "Star card"
        else:
            letters = self.shuffling_letter()
            return random.choice(letters)


    # it will return a list of 10 cards
    def card(self):
        letters = self.shuffling_letter()
        cards = []
        for i in range(1,10):
            random_letter = random.choice(letters)
            cards.append(random_letter)
        cards.append(self.star_card())
        print(cards)
        return cards


    #soriting player cards in alphpitc order

    def quick_sort(self, list1):
        # if the list has 1 or 0 elements, it sorted
        if len(list1) <= 1:
            return list1

        # pivot is the middle element
        pivot = list1[len(list1) // 2]

        # three parts:
        less_than_pivot = [x for x in list1 if x < pivot]
        equal_to_pivot = [x for x in list1 if x == pivot]
        greater_than_pivot = [x for x in list1 if x > pivot]

        # sort the parts and combine togother
        return self.quick_sort(less_than_pivot) + equal_to_pivot + self.quick_sort(greater_than_pivot)

    # generate a three letter or four word
    def word_generater(self):
        while True:
            random_word = random.choice(self.words)
            list1=self.get_valid_transformations(random_word)
            if len(list1) >=2:
                return random_word



    # it can be romoved by interface
    # Check if two words differ by exactly one letter
    def just_one_letter_diff(self, word1, word2):
        diff_count = sum(1 for a, b in zip(word1, word2) if a != b)
        return diff_count == 1

    # check if the word has been changed (is it real or not)
    def check_exists(self,user_word):
        if user_word in self.words:
            return True
        else:
            return False


    #decide who play first
    def coin(self):
        value = random.randint(0, 2)
        if value == 0:
            print("Head")
        else:
            print("Tail")



#test
a=Game()
a.card()










