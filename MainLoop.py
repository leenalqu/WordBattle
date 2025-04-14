# Main loop and game setup, by Leen (5663960)

from GameFunctions import Game #  importing functions
from bot_functions import Bot # importing the bot to use as player 2
import time # importing time to be able to time players
class Player:
    def __init__(self, name, cards=None, streak=0):
        self.name = name
        if cards is None:
            cards = []
        self.cards = cards # player's current stack of cards
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
game = Game() #creating a game interface
player1 = Player(input("Your name: "), game.card()) # asking player 1 for their name
# keeps asking for a difficulty level until a valid answer is given
while True:
    difficulty_level = input("Your difficulty level (easy/medium/hard): ").lower()
    if difficulty_level in ["easy" , "medium" , "hard"]:
        break
    else:
        print("Invalid choice. Please enter the right difficulty level. ")
player2 = Bot(difficulty_level, game.card()) # creating bot player with its cards

# starting the game
result = game.coin() # toss a coin to decide who goes first
if result == "Head":
    current_player = player1
    print(f"{current_player.name} starts the game!") # player starts
else:
    current_player = player2
    print("Bot starts the game!")  # bot starts
current_word = game.word_generater().title() # generates the starting word
print(f"The starting word is: {current_word}")

# main game loop
while True:
    if player1.won_game(): # checks if anyone has won
        print(f"{player1.name} won the game!") # player 1 wins
        winner = player1.name
        break
    elif player2.won_game():
        print("The bot has won the game!") # bot wins
        winner = player2
        break
    if current_player == player1:
        start_time = time.time() # starts the timer
        print(f"{player1.name}, it's you're turn. The word is: {current_word}")
        new_word = input("Enter a new word by changing one letter: ")
        end_time = time.time() #ends the timer
        time_taken = end_time - start_time # calculates the time taken
        if time_taken <= 15: # checking if the player answered in time
            if game.check_exists(new_word): # checks if the new word is valid
                # checks that the word is only 1 letter different
                if game.is_one_letter_dif(current_word, new_word):
                    for i in range(0, 3) : # goes through the letters
                        if current_word[i] != new_word[i]: #find the changed letter
                            changed_letter = new_word[i]
                            if changed_letter in player1.cards: # checks if the player has the letter in their stack
                                player1.remove_cards(changed_letter) # remove it
                                current_word = new_word #update the current word
                                player1.used_words.add(current_word) # add it to used words
                            else:
                                player1.add_card(game.star_card()) # give the player a penalty
                                current_player = player2 # switch turns
        else:
            player1.add_card(game.star_card()) # give a penalty card for taking too long
            current_player = player2 # switch turns

    # bot's turn
    elif current_player == player2:
        print(f"It's the bot's turn. The word is: {current_word}")
        current_timer = 0 # timer for the bot
        bot_word = player2.play_turn(current_word, current_timer) # get the bot's move

        while bot_word == "thinking": # if the bot is still thinking
            time.sleep(1) # wait 1 second
            current_timer += 1 # increase the timer
            bot_word = player2.play_turn(current_word, current_timer) # check again for bot's move
        time.sleep(0.5) # wait a bit to make it feel more natural
        print(f"The bot changed the word to: {bot_word}")

        if game.check_exists(bot_word): # checks if the word is valid
            # checks that the word is only 1 letter different
            if game.is_one_letter_dif(current_word, bot_word):
                for i in range(0, 3): # goes through the letters
                    if current_word[i] != bot_word[i]:
                        changed_letter = bot_word[i]
                        if changed_letter in player2.cards: # checks if the bot has the letter in its stack
                            player2.remove_cards(changed_letter) # remove it
                            current_word = bot_word # update current word
                            player2.used_words.add(current_word) # add it to used words
                        else:
                            player2.add_card(game.star_card()) # give the bot a penalty card
                            current_player = player1 # switch turns
        else:
            player1.add_card(game.star_card()) # bot gets a penalty if the word is invalid
            current_player = player2 # switch turns
