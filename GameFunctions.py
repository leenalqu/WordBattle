import random
import string

# function class game created by Raghad Aljubran (5635869)
"""
this file contains two classes 
1- class game contain 12 functions :
    1-(__init__): for storing the three letter words by using filter
    2-(load_letter_words) take the  words from the file and put them in a list with error hadaling
    3-(valid_transformations): returns a list of valid transformations of a word 
    4-(is_one_letter_dif): used in the validation function
    5-(card_list_and_fisher_shuffle): makes a list of the 28 letters in english and shuffle them
    6-(star_card): returns a star card or a useful letter random for the stack
    7-(card) : uses (card_list_and_fisher_shuffle) and (star_card) to generate 10 cards for the stack
    8-(card_stack): uses (card) to generate a list of 40 cards
    9,10-( partition),(quicksort): algorithm to sort player cards
    11-(word_generator): generates a word for the game and uses (valid_transformations) to check if the word can be changed 2 or more
    12-(check_exists): checks if the word that the player changed is in the words list
    13-(coin) : decide who play first human or bot
    
 2-class Queue : used in the validation function in class Game

"""

#class Queue to be used in the class Game

class Queue:
    def __init__(self):
        self.items=[]

    def append(self, item):
        self.items.append(item)

    def popleft(self):
        if self.items:
            return self.items.pop(0)
        else:
            raise IndexError("the queue is empty")

    def __len__(self):
        return len(self.items)

    def printer(self):
        print(self.items)


# class Game is full of functions that will be called in the main game class
class Game:
    # Initializes the Game class
    def __init__(self):
        #loding all the words in english from a file by calling load letter words function
        self.words = self.load_letter_words("words_alpha.txt")
        # filter out only the three letter words
        self.words = list((filter(lambda word: len(word) == 3, self.words)))

    # Loading the words from a file with error handeling
    def load_letter_words(self, filename):
        try:
            with open(filename, 'r') as file:
                words = {line.strip().lower () for line in file.readlines()}  # Using a set for faster lookup
            return words
        except FileNotFoundError:
            print("File not found.")
            return set()

    # Generate all valid transformations for a word using BFS
    def valid_transformations(self, random_word):
        #using class queue
        queue = Queue()
        queue.append(random_word)
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
        #return a list of valid transformations
        return valid_transformations

    # Check if two words differ by exactly one letter (this function is used in the valid transformations function only)
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

    #Random letter shuffling generator using fisher yates shuffle it return a list of the 28 letters shuffled
    def card_list_and_fisher_shuffle(self):
        letters_list = list(string.ascii_lowercase)
        list_range = range(0, len(letters_list))
        for i in list_range:
            j = random.randint(list_range[0], list_range[-1])
            letters_list[i], letters_list[j] = letters_list[j], letters_list[i]
        return letters_list

    #Function star card (random u might or might not get one if you don't get a star card you will be given a useful letter)
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


    # it will return a list of 10 cards to be used in the stack function
    def card(self):
        letters = self.card_list_and_fisher_shuffle()
        cards = []
        for i in range(0,10):
            random_letter = random.choice(letters)
            cards.append(random_letter)
        cards.append(self.star_card()) # it adds a star card you might not get one instaed a letter
        return cards

    #card stack function returns a list of 40 cards for the game
    def card_stack(self):
        stack = []
        count=40
        while len(stack) < count:
            cards = self.card()  # gets 10 cards including maybe a star
            for c in cards:
                if len(stack) < count:
                    stack.append(c)
        return stack


    #soriting player cards in alphpitc order using quick_sort (need to be called in the main loop every time a new letter is added)
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


    # generate a three letter random word
    def word_generator(self):
        while True:
            random_word = random.choice(self.words)
            word_check=self.valid_transformations(random_word)
            if len(word_check) >=2:
                return random_word


    # check if the word real or not after the player change it
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











