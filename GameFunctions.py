import random
import string
from collections import deque

# function class game created by Raghad

# class Game is full of functions that will be called in the main game class
class Game:
    def __init__(self):
        self.words = self.load_letter_words("words_alpha.txt")
        # Filter out only the three-letter words
        self.words = list((filter(lambda word: len(word) == 3, self.words)))

    # Loading the words from a file
    def load_letter_words(self, filename):
        try:
            with open(filename, 'r') as file:
                words = {line.strip().lower() for line in file.readlines()}  # Using a set for faster lookup
            return words
        except FileNotFoundError:
            print("File not found.")
            return set()

    # Generate all valid transformations using BFS
    def valid_transformations(self, random_word):
        queue = deque([random_word])  #  the start word
        visited = set([random_word])  # Keep track of  words who we vistied
        valid_transformations = []

        while queue:
            word = queue.popleft()

            # Check every possible neighbor with a one letter change
            for n in self.words:
                if n not in visited and self.is_one_letter_dif(word, n):
                    valid_transformations.append(n)
                    visited.add(n)
                    queue.append(n)

        return valid_transformations

    # Check if two words differ by exactly one letter
    def is_one_letter_dif(self, word1, word2):
        if len(word1) != len(word2):
            return False
        c = 0
        for a, b in zip(word1, word2):
            if a != b:
                c += 1
            if c > 1:
                return False
        return c == 1

    #Random letter shuffling generator using fisher yates shuffle
    def card_list_and_fisher_shuffle(self):
        letters_list = list(string.ascii_lowercase)
        list_range = range(0, len(letters_list))
        for i in list_range:
            j = random.randint(list_range[0], list_range[-1])
            letters_list[i], letters_list[j] = letters_list[j], letters_list[i]
        return letters_list

    #Function star card (random u might or might not get one if you dont get a star card you will be given a usefil letter)
    def star_card(self):
        value = random.randint(0, 1)
        if value == 0:
            return "Star card"
        else:
            l=random.randint(1, 3)
            if l == 1:
                return "e"
            elif l == 2:
                return "a"
            else:
                return "t"



    # it will return a list of 10 cards to be used in the stack
    def card(self):
        letters = self.card_list_and_fisher_shuffle()
        cards = []
        for i in range(0,10):
            random_letter = random.choice(letters)
            cards.append(random_letter)
        cards.append(self.star_card()) # it adds a star card you might not get one instaed a letter
        return cards

    def create_card_stack(self):
        stack = []
        count=40
        while len(stack) < count:
            cards = self.card()  # gets 10 cards including maybe a star
            for c in cards:
                if len(stack) < count:
                    stack.append(c)
        return stack


    #soriting player cards in alphpitc order using quick_sort (need to be called in the main loop)
    def partition(self,list1, low, high):

        pivot = list1[high]
        i = low - 1

        for j in range(low, high):
            if list1[j] <= pivot:
                i += 1
                list1[i], list1[j] = list1[j], list1[i]

        list1[i + 1], list1[high] = list1[high], list1[i + 1]
        return i + 1

    def quicksort(self,list1, low=0, high=None):
        if high is None:
            high = len(list1) - 1

        if low < high:
            pivot_index = self.partition(list1, low, high)
            self.quicksort(list1, low, pivot_index - 1)
            self.quicksort(list1, pivot_index + 1, high)


    # generate a three letter random word with valied transformations check
    def word_generater(self):
        while True:
            random_word = random.choice(self.words)
            word_check=self.valid_transformations(random_word)
            if len(word_check) >=2:
                return random_word


    # check if the word real or not
    def check_exists(self,user_word):
        if user_word in self.words:
            return True
        else:
            return False

    #decide who play first
    def coin(self):
        value = random.randint(0, 1)
        if value == 0:
            print("Head")
        else:
            print("Tail")



#test
a=Game()
print(a. word_generater())










