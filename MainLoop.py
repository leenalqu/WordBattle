# Main loop and game setup, by Leen (5663960).


# Import time to be able to time players
import time

# Import functions
from GameFunctions import Game

# Import the bot to use as player 2.
from BotFunctions import Bot


class Player:
    """
    A human player that plays against a bot.

    Attributes
    ----------
    name : str
        The player's name.
    cards : list
        The player's letter cards.
    used_words : set
        The words that the player has used.
    """
    def __init__(self, name, cards=None):
        """
        Initializing a player's instance.

        Parameters
        ----------
        name : str
            Player's name.
        cards : list
            Player's letter cards, defaults to empty list.
        """
        self.name = name
        if cards is None:
            cards = []

        # The player's current stack of cards.
        self.cards = cards

        # A set of the words that have been used by the player.
        self.used_words = set()

    # Add a letter to the player's stack of cards.
    def add_card(self, letter):
        """
        Adds a card to the player's letter cards.

        Parameters
        ----------
        letter : str
            The letter to add to the player's letter cards.
        """
        self.cards.append(letter)

    # Remove a letter from the player's cards.
    def remove_cards(self, letter):
        """
        Removes a card from the player's letter cards.

        Parameters
        ----------
        letter : str
            The letter to remove from the player's letter cards.
        """

        # Make sure the letter exists.
        if letter in self.cards:
            self.cards.remove(letter)
        elif "*" in self.cards:
            self.cards.remove("*")

    # Checks if the player has used all of their cards.
    def won_game(self):
        """
        Checks if the player has used all of their cards.

        Returns
        --------
        Bool:
            True if player has used all of their cards, otherwise False.
        """

        # The winner is announced when they finish all their cards.
        return len(self.cards) == 0

# The game setup.
game = Game()
deck = game.card_stack()
used_cards = []

# Pass cards for player 1 and player 2.
player1_cards = [deck.pop() for _ in range(7)]
player2_cards = [deck.pop() for _ in range(7)]

# Create player 1 using input name.
player1 = Player(input("Your name: "), player1_cards)

# Keep asking for a difficulty level until a valid answer is given.
while True:
    difficulty_input= input("Your difficulty level (easy/medium/hard): ").lower()
    if difficulty_input in ["easy" , "medium" , "hard"]:
        difficulty_enum = Bot.Difficulty[difficulty_input.upper()]
        break
    else:
        print("Invalid choice. Please enter the right difficulty level. ")

# Create a bot player with its cards.
player2 = Bot(difficulty_enum, player2_cards)

# Start the game.
# Toss a coin to decide who goes first.
result = game.coin_flip()

# Determine who goes first based on the result.
if result == "Head":
    current_player = player1

    # Player1 starts.
    print(f"{current_player.name} starts the game!")
else:
    current_player = player2

    # The bot starts.
    print("Bot starts the game!")

# Generate the starting word.
current_word = game.word_generator().title()
print(f"The starting word is: {current_word}")

# Main game loop.
while True:

    # Check if anyone has won.
    if player1.won_game():

        # Player1 wins.
        print(f"{player1.name} won the game!")
        winner = player1.name
        break
    elif player2.won_game():

        # Bot wins.
        print("The bot has won the game!")
        winner = player2
        break
    if current_player == player1:
        print(f"Your current cards: {player1.cards}")

        # Start the timer.
        start_time = time.time()
        print(f"{player1.name}, it's your turn. The word is: {current_word}")
        new_word = input("Enter a new word by changing one letter: ")

        # End the timer.
        end_time = time.time()

        # Calculate the time taken.
        time_taken = end_time - start_time

        # Check if the player answered within 15 seconds.
        if time_taken <= 15:

            # Check if the new word is valid and differs by 1 letter.
            if game.check_exists(new_word) and game.is_one_letter_dif(
                    current_word, new_word
            ):
                changed = False

                # Go through the letters.
                for i in range(3) :

                    # Find the changed letter.
                    if current_word[i] != new_word[i]:
                        changed_letter = new_word[i]

                        # Check if the player has the letter in their stack.
                        if changed_letter in player1.cards or "*" in player1.cards:
                            player1.remove_cards(changed_letter)
                            game.quicksort(player1.cards)
                            used_cards.append(changed_letter)

                            # Update the current word.
                            current_word = new_word

                            # Switch turns.
                            current_player = player2
                            print("It is now the bot's turn.")

                            # Add it to used words.
                            player1.used_words.add(current_word)
                            changed = True
                            break
                if not changed:
                    if not deck:
                        deck = game.fisher_shuffle(used_cards.copy())
                        used_cards = []

                    # Give the player a penalty.
                    player1.add_card(deck.pop())
                    print(f"{player1.name} got a penalty card.")
                    game.quicksort(player1.cards)

                    # Switch turns.
                    current_player = player2

            else:

                # The player entered an invalid word.
                if not deck:

                    # Shuffle used cards and put them back into the deck.
                    deck = game.fisher_shuffle(used_cards.copy())
                    used_cards = []
                player1.add_card(deck.pop())
                print(f"{player1.name} entered an invalid word.")
                game.quicksort(player1.cards)

                # Switch turns.
                current_player = player2
        else:

            # The player took too long.
            if not deck:

                # Shuffle used cards and put them back into the deck.
                deck = game.fisher_shuffle(used_cards.copy())
                used_cards = []
            player1.add_card(deck.pop())
            print(f"{player1.name} got a penalty card for taking too long.")
            game.quicksort(player1.cards)
            current_player = player2


    # Bot's turn.
    elif current_player == player2:
        print(f"Bot's current cards: {player2.cards}")
        print(f"It's the bot's turn. The word is: {current_word}")
        # inside if loop

        # Timer for the bot.
        current_timer = 0

        # Get the bot's move.
        bot_word = player2.play_turn(current_word, current_timer)

        # If the bot is still thinking.
        while bot_word == Bot.Output.THINKING:

            # Wait 1 second.
            time.sleep(1)

            # Increase the timer.
            current_timer += 1

            # Check again for bot's move.
            bot_word = player2.play_turn(current_word, current_timer)

        # Handles bot_word when it's a tuple.
        if isinstance(bot_word, tuple):
            bot_answer, bot_used_card = bot_word
        else:
            bot_answer = bot_word

        if not bot_answer:
            if not deck:
                deck = game.fisher_shuffle(used_cards.copy())
                used_cards = []
            player2.add_card(deck.pop())
            print("The bot failed to change the word.")
            game.quicksort(player2.cards)
            current_player = player1
            player2.end_turn()
            continue

        # Wait a bit to make it feel more natural.
        time.sleep(0.5)
        changed = False

        # Check if the word is valid and differs by only 1 letter.
        if bot_answer and game.check_exists(bot_answer) and game.is_one_letter_dif(
                current_word, bot_answer
        ):

                # Go through the letters.
            for i in range(3):
                if current_word[i] != bot_answer[i]:
                    changed_letter = bot_answer[i]

                    # Check if the bot has the letter in its stack.
                    if changed_letter in player2.cards or "*" in player2.cards:
                        player2.remove_cards(changed_letter)
                        game.quicksort(player2.cards)
                        used_cards.append(changed_letter)

                        # Update current word.
                        current_word = bot_answer
                        print(f"The bot changed the word to {bot_answer} ")
                        print(f"The current word is: {current_word}")
                        current_player = player1
                        player2.end_turn()
                        changed = True
                        break
            if not changed:
                if not deck:
                    deck = game.fisher_shuffle(used_cards.copy())
                    used_cards = []

                # Give the bot a penalty card.
                player2.add_card(deck.pop())
                print("The bot got a penalty card")
                game.quicksort(player2.cards)

                # Switch turns.
                current_player = player1
                player2.end_turn()
        else:
            if not deck:
                deck = game.fisher_shuffle(used_cards.copy())
                used_cards = []

            # Bot gets a penalty if the word is invalid.
            player2.add_card(deck.pop())
            print("Bot got a penalty card.")
            game.quicksort(player2.cards)

            # Switch turns.
            current_player = player1
            player2.end_turn()