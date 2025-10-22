# WORD BATTLE

# Implemented Algorithms:
- Fisher Yates [Game().fisher_shuffle()]
- Quick Sort [Game().quicksort()]
- Insertion Sort [Bot().letter_frequency_sort()]
- Graph BFS [Game().valid_transformations() and Bot()._next_word()]
 
# Implemented data structures:
- Graph [Represented by the sets: Game().words & Bot()._bot_words]
- Queue
 
# Uncommon data types:
- Enum [Bot.Difficulty and Bot.Output]
 
# Programming Techniques:
- Graphical Interface [pygame]
- OOP [Classes]
- Modules
- JSON file loading
- lambda
- filter
- Annotations

# Debugging:
- Raising Exceptions
- Exception Handling
- Print Statements

# My Role and Contributions:
- Implemented main game loop and turn logic.
- Developed:
  * Card interaction and reorganization system.
  * Penalty card distribution.
  * Managed player and bot turn switching logic.
  * Integrated timer functionality for turn timeouts.
  * Implemented word validation and transformation checks.
  * Developed win condition detection.
  * Standardized code style for consistency.
  * Assisted with game logic integration.


# Game Overview:
   [ The Word Battle 🃏
    welcome to our game the high risk card game 
    where letters are your bullets and words are your weapons
    and your mined is your greatest ally.Ready Let’s go! ]

# Game Basics (●'◡'●):
1. Deck Size: 40 letter cards
2. Players: You🧍 vs computer 🤖
3. Starting Cards: Each player gets 7 random letter cards and possibly Star Card ✨
4. Starting Word: random 3-letter word

# How to play🤔:
1. player takes turns 🔁
2. On each turn there will be a 15 seconds timer ⏱️ to change
   ONE letter in the current word to form a new valid word.
3. In that time the player must change ONE letter in the current
    word by using one of their letter cards to form a new valid word

# Penalties ❗:
## A new card will be given to you do on of these :
1. Didn’t make a move in time ⏰
2. Played invalid word 

## Reached 15 cards?? You’re out. Game over ☠️

# Star Card Power ⭐:
1. Use Star Card anytime to replace any one letter in the word with a ⭐ wildcard.
2. Star cards are useful if you are stuck and can’t change the current word with your
    letters because it will change the current word to a new random word
3. The computer will try every alphabet letter in that position of the star card to
    find a real word.
4. If no real word is found, you get a Penalty card! 😈

# Bot Levels 💪:
🟢 Level 1: Easy 
🟡 Level 2: Medium
🔴 Level 3: Hard

# Win Rewards🏆:
For every time you change a word you will earn a point if you reach 3 points you 
can remove 1 card from your hand. This is useful to remove difficult words 😊

# How to Win:
1. Every time you make a valid word you get rid of 1 card 😜
2. First to zero cards wins the game 😍🎉🏆
3. If either you or the computer collects 15 cards, that player
    will be out of the game ☠️😵‍💫

# Coin Flip (Who Goes First?)🪙
At the start of the game a coin flip decides who makes the first move 
wish luck to be on your side 😊

##### Ready???? Let’s go 🤗

[View the original group repository](https://github.com/hasanwazzan5/WordBattle)





   
    
                 









        
    









