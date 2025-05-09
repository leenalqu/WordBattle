# Functions class game created by Raghad Aljubran (5635869).

#importing built-in libraries
import random
import string
#importing custom module
from GameSettings import GameSettings

# Class Queue to be used in the class Game.
class Queue:
    """
    class Queue : used in the validation function in class Game
    """
    def __init__(self):
        self.items=[]

    def append(self,item):
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


# Class Game is full of functions that will be called in the main game class.
class Game:
    """
    This class contain functions to be used in the game loop and interface.

    1- class game contain 12 functions :
        1-(__init__): for storing the three letter words by using filter.

        2-(load_letter_words): take the  words from the file and put them in a list
            with error handling.

        3-(valid_transformations): returns a list of valid transformations
            of a word.

        4-(is_one_letter_dif): takes two words and compare them if they differ
            by one letter only.

        5-(fisher_shuffle): shuffles a list using fisher algorithm.

        6-(star_card): returns a star card or a useful letter random for the
            stack.

        7-(card_stack): generate a stack of 40 cards uses two functions
            (fisher_shuffle and star_card).

        8,9-( partition),(quicksort): algorithm to sort player cards.

        10-(word_generator): generates a word for the game and uses (valid_transformations)
            to check if the word can be changed 4 or more.

        11-(check_exists): checks if the word that the player changed is in the words list
            and it handel both word with a star and word without a star.

        12-(coin_flip) : decide who play first human or bot.

    """

    # Initializes the Game class.
    def __init__(self):
        """
        For storing the three letter words by using filter.
        """
        # Creating an object for game settings class
        self.object_settings=GameSettings()
        # Lode all the words in english from a file by calling load letter words function.
        self.words = self.load_letter_words("data/words_alpha.txt")
        # Filter out only the three letters words.
        self.words = list((filter(lambda word:len(word) ==self.object_settings.WORD_LENGTH,self.words)))


    # Loading the words from a file with error handel.
    def load_letter_words(self, filename):
        """
         Take the words from the file and put them in a list
            with error handling.
        """
        try:
            with open(filename,'r') as file:
                words = {line.strip().lower () for line in file.readlines()}  # Using a set for faster lookup.
            return words
        except FileNotFoundError:
            print("File not found.")
            return set()

    # Generate all valid transformations for a word using BFS.
    def valid_transformations(self,random_word):
        """
        Returns a list of valid transformations of a word.
        """
        # Using class queue.
        queue = Queue()
        queue.append(random_word)
        visited = set([random_word])  # Keep track of words that are visited.
        valid_transformations = []

        while queue:
            word = queue.popleft()

            # Check every possible neighbor with a one letter change.
            for n in self.words:
                if n not in visited and self.is_one_letter_dif(word,n):
                    valid_transformations.append(n)
                    visited.add(n)
                    queue.append(n)
        # Return a list of valid transformations.
        return valid_transformations

    # Check if two words differ by exactly one letter.
    def is_one_letter_dif(self,word1,word2):
        """
        Takes two words and compare them if they differ
            by one letter only.
        """
        if len(word1) != len(word2):
            return False
        if word1 == word2:
            return False
        c = 0
        for a,b in zip(word1,word2):
            if a!= b:
                c += 1
            if c > 1:
                return False
        return True

    # Shuffling generator using fisher yates shuffle.
    def fisher_shuffle(self,cards):
        """
        Shuffles a list using fisher algorithm.
        """
        for i in range(len(cards) - 1,0,-1):
            j = random.randint(0,i)
            cards[i],cards[j] = cards[j],cards[i]
        return cards

    # Function star card random u might or might not get a * if you don't get a star card you will be given a useful letter.
    def star_card(self):
        """
        Returns a star card or a useful letter random for the stack.
        """
        value = random.randint(0,10)
        if value <=7:
            return "*"
        else:
            l=random.randint(1,3)
            if l == 1:
                return "e"
            elif l == 2:
                return "a"
            else:
                return "t"

    # Function will return a list of 40 cards shuffled.
    def card_stack(self):
        """
        Generate a stack of 40 cards uses two functions
            (fisher_shuffle and star_card).
        """
        letters = list(string.ascii_lowercase)
        list_range = range(0,len(letters))
        cards = []
        for i in range(0,34):
            random_letter = random.choice(letters)
            cards.append(random_letter)
        for i in range(0,6):
            cards.append(self.star_card())  # it adds a * card you might  get * or useful letter
        return self.fisher_shuffle(cards)

    # Sorting player cards in alphabet order using quick sort algorithm(need to be called in the main loop every time a new letter is added).
    def partition(self,list1,low,high):
        """
        Algorithm to sort player cards.
        """
        pivot = list1[high]
        i = low - 1

        for j in range(low,high):
            if list1[j] <= pivot:
                i += 1
                list1[i],list1[j] = list1[j],list1[i]

        list1[i + 1],list1[high] = list1[high],list1[i + 1]
        return i + 1

    def quicksort(self,list1,low=0,high=None):
        """
        Algorithm to sort player cards.
        """
        if high is None:
            high = len(list1) - 1

        if low < high:
            pivot_index = self.partition(list1,low,high)
            self.quicksort(list1,low,pivot_index - 1)
            self.quicksort(list1,pivot_index + 1,high)

    # Generate a three letter random word.
    def word_generator(self):
        """
        Generates a word for the game and uses (valid_transformations)
            to check if the word can be changed 4 or more.
        """
        vowels ='aeiou'  # List of vowels.
        while True:
            random_word = random.choice(self.words)
            if random_word[1] in vowels:
                word_check=self.valid_transformations(random_word)
                if len(word_check) >=4:
                    return random_word

    # Check if the word real or not after the player change it.
    def check_exists(self,player_word):
        """
        Checks if the word that the player changed is in the words list
            and it handel both word with a star and word without a star.
        """
        if "*" in player_word:
            for i in range(97,123):  # Letters from the letter a to letter z.
                letter=chr(i)
                check_word=player_word.replace("*",chr(i),1) # It is replacing the star with letter.
                if check_word in self.words:
                    return True
            return False
        else:
            if player_word in self.words:
                return True
            else:
                return False

    # Decide who play first.
    def coin_flip(self):
        """
        Decide who play first human or bot
        """
        value = random.randint(0,1)
        if value == 0:
            return "Head"
        else:
            return "Tail"


