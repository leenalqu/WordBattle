# Main loop and game setup, by Leen (5663960)

from GameFunctions import Game #  importing functions
from bot_functions import Bot # importing the bot to use as player 2
class Player:
    def __init__(self, name, cards=None, streak=0):
        self.name = name
        if cards is None:
            cards = []
        self.cards = cards
        self.streak = streak # the number of continuous wins
        self.used_words = set() # a set of the words that have been used by the player
    def add_card(self, letter): # adds a letter to player's stack of cards
        self.cards.append(letter)
    def remove_cards(self, letter): # removes a letter from player's stack of cards
        if letter in self.cards: # makes sure the letter exists
            self.cards.remove(letter)
    def won_game(self):
        return len(self.cards) == 0 # the winner is announced when they finish all their cards

# game setup
game = Game()
player1 = Player(input("Your name: "), game.card())
while True:
    difficulty_level = input("Your difficulty level (easy/medium/hard): ").lower()
    if difficulty_level in ["easy" , "medium" , "hard"]:
        break
    else:
        print("Invalid choice. Please enter the right difficulty level. ")
player2 = Bot(difficulty_level, game.card())

# starting the game
result = game.coin()
if result == "Head":
    current_player = player1
    print(f"{current_player.name} starts the game!")
else:
    current_player = player2
    print("Bot starts the game!")



