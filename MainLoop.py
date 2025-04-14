# Main loop and game setup, by Leen (5663960)

from GameFunctions import Game #  importing functions
from BotFunctions import Bot # importing the bot to use as player 2
import time
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

current_word = game.word_generater().title()
print(f"The starting word is: {current_word}")

while True:
    if player1.won_game():
        print(f"{player1.name} won the game!")
        winner = player1.name
        break
    elif player2.won_game():
        print("The bot has won the game!")
        winner = player2
        break
    if current_player == player1:
        start_time = time.time()
        print(f"{player1.name}, it's you're turn. The word is: {current_word}")
        new_word = input("Enter a new word by changing one letter: ")
        end_time = time.time()
        time_taken = end_time - start_time
        if time_taken <= 15:
            if game.check_exists(new_word):
                if game.is_one_letter_dif(current_word, new_word):
                    for i in range(0, 3) :
                        if current_word[i] != new_word[i]:
                            changed_letter = new_word[i]
                            if changed_letter in player1.cards:
                                player1.remove_cards(changed_letter)
                                current_word = new_word
                                player1.used_words.add(current_word)
                            else:
                                player1.add_card(game.star_card())
                                current_player = player2
        else:
            player1.add_card(game.star_card())
            current_player = player2

    elif current_player == player2:
        print(f"It's the bot's turn. The word is: {current_word}")
        current_timer = 0
        bot_word = player2.play_turn(current_word, current_timer)
        while bot_word == "thinking":
            time.sleep(1)
            current_timer += 1
            bot_word = player2.play_turn(current_word, current_timer)
        time.sleep(0.5)
        print(f"The bot changed the word to: {bot_word}")
        if game.check_exists(bot_word):
            if game.is_one_letter_dif(current_word, bot_word):
                for i in range(0, 3):
                    if current_word[i] != bot_word[i]:
                        changed_letter = bot_word[i]
                        if changed_letter in player2.cards:
                            player2.remove_cards(changed_letter)
                            current_word = bot_word
                            player2.used_words.add(current_word)
                        else:
                            player2.add_card(game.star_card())
                            current_player = player1
        else:
            player1.add_card(game.star_card())
            current_player = player2
