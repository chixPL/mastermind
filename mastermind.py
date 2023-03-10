"""
Mastermind implementation in Python
by Jakub Rutkowski (chixPL) 2023

When the program starts, you can choose between two possible modes.
"Game mode" is designed to simulate the game game as closely as possible and it's a mode where a human player plays against a computer.

Game mode rules:
- 4-peg code to determine
- 4 result pegs (black and white)
- 10 tries
- 8 colours (red, green, blue, yellow, violet, olive, pink, teal)
- Two result colors:
    Black (denoted with K) = The peg is in the correct place
    White (W) = The peg is in the code but is in the wrong place
- Game against a computer

The algorithm mode uses a simplified version of the game as defined in Knuth's original paper. The source is available in the README.

Algorithm mode rules:
- 4-peg code to determine
- 4 result pegs (black and white)
- Unlimited number of tries
- 6 colours, simplified as numbers
- Two result colors:
    Black (denoted with K) = The peg is in the correct place
    White (W) = The peg is in the code but is in the wrong place
- Computer plays against itself with the goal of minimizing required turns


Created with Python 3.10.6 and the standard library.

"""
import random
import itertools
import time

class Mastermind:

    def __init__(self) -> None:
        self.c_deck = [] # Computer deck
        self.gameEnd = False # Game end variable
        self.turns = 0 # Turn counter
        self.mode = '' # Game or algorithm mode
        self.start_game()
    
    def start_game(self):
        print("*" * 20)
        print("Welcome to Mastermind") 
        print("*" * 20)
        print("\n")

        while(True):
            print("Select game mode:")
            print("a: Player vs CPU")
            print("b: Algorithm (CPU vs CPU)")
            print("*" * 20)
            self.mode = input() # The user's choice of mode (a=game, b=algorithm)
            if self.mode not in ['a','b']:
                print("Wrong mode choice!")
            else:
                break

        if self.mode == 'a':
            self.colours = ['R','G','B','Y','V','O','P','T']
            self.create_deck('game') # Create a computer deck in game mode
            while(self.gameEnd == False):
                if(self.turns == 10):
                    print("You lost.")
                    exit()
                else:
                    self.player_turn() 
        else:
            self.create_deck('cpu') # Create a computer deck in the simplified algorithm mode
            self.algo()

    def randomize(self, mode):
        deck = []
        if mode == 'game':
            elems = self.colours # Use the colours array to stay true to the board game's rules
        else:
            elems = []
            for i in range(1, 6):
                elems.append(i) # Use numbers for better mathematical clarity for the algorithm mode
        for i in range(4):
            colour = random.choice(elems)
            deck.append(colour)
            elems.remove(colour)
        return tuple(deck)


    def create_deck(self, mode):
        self.c_deck = self.randomize(mode)

    def player_turn(self): # User input loop
        while(True):
            guesses = input("Enter a sequence of 4 pegs separated by spaces: ")
            guesses = guesses.upper().split(' ')
            if len(guesses) != 4:
                print("Wrong input!")
            else:
                self.check(guesses)
                break

    def check(self, input):
        self.answers = []
        """
        Checking for every peg:
        If the color and the index match, it's a black peg.
        If only the color matches (it's in the c_deck array but in the wrong place), it's a white peg.
        If there's no peg with the chosen color, return an empty string. 
        """
        if self.mode == 'a': # Game mode
            for i in range(0, len(input)):
                if input[i] == self.c_deck[i]:
                    self.answers.append('K')
                elif input[i] in self.c_deck:
                    self.answers.append('W')
                else:
                    self.answers.append('')
            if self.answers == ['K', 'K', 'K', 'K']: # If all pegs in the checking deck are black, end the game
                self.gameEnd = True
                print("You won!")
                exit()
            else:
                self.answers = sorted(self.answers, key=lambda x: (x == "", x.lower())) 
                """
                ^^^ This uses ASCII code manipulation to sort but have empty strings at the end. 
                It makes it more readable to the end user.
                """
                print(self.answers)
        else: # Algorithm mode
            # The colors are represented by numbers for better mathematical clarity. Unlike in the game mode, the pegs aren't counted because they exist only for the users' clarity.
            blacks = 0
            whites = 0
            for i in range(0, len(input)):
                if input[i] == self.c_deck[i]:
                    blacks += 1
                elif input[i] in self.c_deck:
                    whites += 1
            
            return (blacks,whites)

    def check_all(self, moves, response):
        """
        Algorithm mode only.
        Check the entire moves array against the code-maker's input in order to eliminate impossible moves.
        """
        for i in moves:
            blacks = 0
            whites = 0
            for j in range(0, 4):
                if i[j] == self.c_deck[j]:
                    blacks += 1
                elif i[j] in self.c_deck:
                    whites += 1

            if((blacks,whites) != response and (blacks,whites) != (4, 0)):
                moves.remove(i)
        return moves
    
    def score(self, moves):
        """
        Algorithm mode only.
        Knuth follows the convention of choosing the guess with the least numeric value; e.g., 2345 is lower than 3456.
        Therefore, the move with the lowest sum is always selected.
        """
        scores = []
        for i in moves:
            scores.append(sum(i))
        return scores
    
    def algo(self):
        self.start_time = time.time()
        self.colours = [i for i in range(1, 7)] # Using numbers for better mathematical clarity.
        print("You're in algorithm mode.")
        self.c_deck = (self.randomize('cpu'))
        print("CPU: ",self.c_deck)
        moves = list(itertools.product(self.colours, repeat=4)) # 1296 (6^4) codes are possible in Knuth's standardized game version.
        self.p_deck = (1, 1, 2, 2)

        rounds = 0

        while(self.gameEnd != True):
            result = self.check(self.p_deck)
            rounds += 1
            if(result != (4,0)):
                moves = self.check_all(moves, result)
                print("-----------------")
                print(f"CPU: {self.c_deck}")
                print(f"Moves: {moves}")
                scores = self.score(moves) 
                self.p_deck = moves[scores.index(min(scores))] # Determines the next move to be checked with the code makers
                moves.remove(self.p_deck)
                print(f"Player Choice: {self.p_deck}") 
            else:
                print(f"The computer has cracked the code in {rounds} rounds | Execution time: {time.time() - self.start_time}")
                self.gameEnd = True
                exit()

# Start game
game = Mastermind()