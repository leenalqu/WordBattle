# Main loop and game setup, by Leen (5663960).

import time # Importing time to be able to time players
from GameFunctions import Game # Importing functions
from BotFunctions import Bot # Importing the bot to use as player 2.


class Player:
    """
    A human player that plays against a bot.

    Attributes
    ----------
    name : str
        The player's name.
    cards : list
        The player's letter cards.
    streak : int
        The player's win streak.
    used_words : set
        The words that the player has used.
    """
    def __init__(self, name, cards=None, streak=0):
        """
        Initializing a player's instance.

        Parameters
        ----------
    name : str
        Player's name.
    cards : list
        Player's letter cards, defaults to empty list.
    streak : int
        Player's win streak, defaults to 0.
        """
        self.name = name
        if cards is None:
            cards = []
        self.cards = cards # The player's current stack of cards.
        self.streak = streak # The number of continuous wins.
        self.used_words = set() # A set of the words that have been used by the player.
    def add_card(self, letter): # Adds a letter to the player's stack of cards.
        """
        Adds a card to the player's letter cards.

        Parameters
        ----------
        letter : str
            The letter to add to the player's letter cards.
        """
        self.cards.append(letter)
    def remove_cards(self, letter): # Removes a letter from player's stack of cards.
        """
        Removes a card from the player's letter cards.

        Parameters
        ----------
        letter : str
            The letter to add to the player's letter cards.
        """
        if letter in self.cards: # Makes sure the letter exists.
            self.cards.remove(letter)
    def won_game(self):
        """
        Checks if the player has used all of their cards.

        returns
        --------
        Bool:
            True if player has used all of their cards, otherwise False.
        """
        return len(self.cards) == 0 # The winner is announced when they finish all their cards.

# The game setup.
game = Game() # Creating the game's interface.
deck = game.card_stack()
used_cards = []
player1_cards = [deck.pop() for _ in range(7)]
player2_cards = [deck.pop() for _ in range(7)]
player1 = Player(input("Your name: "), player1_cards) # Asking player 1 for their name.

# Keeps asking for a difficulty level until a valid answer is given.
while True:
    difficulty_input= input("Your difficulty level (easy/medium/hard): ").lower()
    if difficulty_input in ["easy" , "medium" , "hard"]:
        difficulty_enum = Bot.Difficulty[difficulty_input.upper()]
        break
    else:
        print("Invalid choice. Please enter the right difficulty level. ")
player2 = Bot(difficulty_enum, player2_cards) # creating bot player with its cards

# Starting the game.
result = game.coin_flip() # Tosses a coin to decide who goes first.
if result == "Head":
    current_player = player1
    print(f"{current_player.name} starts the game!") # Player1 starts.
else:
    current_player = player2
    print("Bot starts the game!")  # Bot starts.
current_word = game.word_generator().title() # Generates the starting word.
print(f"The starting word is: {current_word}")

# main game loop
while True:
    if player1.won_game(): # Checks if anyone has won.
        print(f"{player1.name} won the game!") # Player1 wins.
        winner = player1.name
        break
    elif player2.won_game():
        print("The bot has won the game!") # Bot wins.
        winner = player2
        break
    if current_player == player1:
        print(f"Your current cards: {player1.cards}")
        start_time = time.time() # Starts the timer.
        print(f"{player1.name}, it's you're turn. The word is: {current_word}")
        new_word = input("Enter a new word by changing one letter: ")
        end_time = time.time() # Ends the timer
        time_taken = end_time - start_time # Calculates the time taken.
        if time_taken <= 15: # Checks if the player answered in time.
            if game.check_exists(new_word): # Checks if the new word is valid.
                # Checks that the word is only 1 letter different.
                if game.is_one_letter_dif(current_word, new_word):
                    for i in range(0, 3) : # Goes through the letters.
                        if current_word[i] != new_word[i]: # Finds the changed letter.
                            changed_letter = new_word[i]
                            if changed_letter in player1.cards: # Checks if the player has the letter in their stack
                                player1.remove_cards(changed_letter) # Removes it.
                                game.quicksort(player1.cards)
                                used_cards.append(changed_letter)
                                current_word = new_word # Updates the current word.
                                player1.used_words.add(current_word) # Adds it to used words.
                                current_player = player2
                            else:
                                if not deck:
                                    deck = game.fisher_shuffle(used_cards.copy())
                                    used_cards = []
                                player1.add_card(deck.pop()) # Give the player a penalty.
                                game.quicksort(player1.cards)
                                current_player = player2 # Switch turns
        else:
            if not deck:
                deck = game.fisher_shuffle(used_cards.copy())
                used_cards = []
            player1.add_card(deck.pop()) # Give a penalty card for taking too long.
            game.quicksort(player1.cards)
            current_player = player2 # Switch turns.

    # bot's turn
    elif current_player == player2:
        print(f"Your current cards: {player2.cards}")
        print(f"It's the bot's turn. The word is: {current_word}")
        current_timer = 0 # timer for the bot
        bot_word = player2.play_turn(current_word, current_timer) # Get the bot's move.

        while bot_word == Bot.Output.THINKING: # If the bot is still thinking.
            time.sleep(1) # Wait 1 second
            current_timer += 1 # increase the timer.
            bot_word = player2.play_turn(current_word, current_timer) # Check again for bot's move.
        time.sleep(0.5) # Wait a bit to make it feel more natural.
        print(f"The bot changed the word to: {bot_word}")
        print(f"New current word is: {current_word}")

        if game.check_exists(bot_word): # Checks if the word is valid.
            # Checks that the word is only 1 letter different.
            if game.is_one_letter_dif(current_word, bot_word):
                for i in range(0, 3): # Goes through the letters.
                    if current_word[i] != bot_word[i]:
                        changed_letter = bot_word[i]
                        if changed_letter in player2.cards: # Checks if the bot has the letter in its stack.
                            player2.remove_cards(changed_letter) # Remove it
                            game.quicksort(player2.cards)
                            used_cards.append(changed_letter)
                            current_word = bot_word # Updates current word.
                            current_player = player1
                            player2.end_turn()
                        else:
                            if not deck:
                                deck = game.fisher_shuffle(used_cards.copy())
                                used_cards = []
                            player2.add_card(deck.pop()) # Gives the bot a penalty card.
                            game.quicksort(player2.cards)
                            current_player = player1 # Switch turns
                            player2.end_turn()
        else:
            if not deck:
                deck = game.fisher_shuffle(used_cards.copy())
                used_cards = []
            player2.add_card(deck.pop()) # Bot gets a penalty if the word is invalid.
            game.quicksort(player2.cards)
            current_player = player1 # Switch turns
            player2.end_turn()
