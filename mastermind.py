"""
Gra Mastermind z komputerem
Zasady:
- 4 kolumny
- 4 pola sprawdzające
- 10 prób
- 8 kolorów (red, green, blue, yellow, violet, olive, pink, teal)
- 2 kolory sprawdzające (white, blacK)
- gra z komputerem
"""
import random
import itertools
import time

class Mastermind:

    def __init__(self) -> None:
        self.c_deck = [] # talia komputera
        self.gameEnd = False # koniec gry
        self.tryb = ''
        self.start_game()
    
    def start_game(self):
        print("*" * 20)
        print("Witamy w Mastermindzie") 
        print("*" * 20)
        print("\n")

        while(True):
            print("Wybierz tryb gry: ")
            print("a: Gracz vs Komputer")
            print("b: Algorytm (Komputer vs Komputer)")
            print("*" * 20)
            self.tryb = input()
            if self.tryb not in ['a','b']:
                print("Źle wybrałeś tryb!")
            else:
                break

        if self.tryb == 'a':
            self.colours = ['R','G','B','Y','V','O','P','T']
            self.create_deck()
            while(self.gameEnd == False):
                self.player_turn()
        else:
            self.create_deck('cpu')
            self.algo()

    def randomize(self, mode="real"):
        deck = []
        if mode == 'real':
            elems = self.colours
        else:
            elems = []
            for i in range(1, 6):
                elems.append(i)
        for i in range(4):
            colour = random.choice(elems)
            deck.append(colour)
            elems.remove(colour)
        return tuple(deck)


    def create_deck(self, mode):
        self.c_deck = self.randomize(mode)

    def player_turn(self):
        while(True):
            guesses = input("Wybierz 4 kule oddzielone spacją: ")
            guesses = guesses.upper().split(' ')
            if len(guesses) != 4:
                print("Źle wpisałeś!")
            else:
                self.check(guesses)
                break

    def check(self, input):
        self.answers = []
        if self.tryb == 'a':
            for i in range(0, len(input)):
                if input[i] == self.c_deck[i]:
                    self.answers.append('K')
                elif input[i] in self.c_deck:
                    self.answers.append('W')
                else:
                    self.answers.append('')
            if(all(list(filter(lambda x: x=='K', self.answers)))):
                self.gameEnd = True
                print("Wygrałeś!")
                exit()
            else:
                self.answers = sorted(self.answers, key=lambda x: (x == "", x.lower()))
                print(self.answers)
        else:
            blacks = 0
            whites = 0
            for i in range(0, len(input)):
                if input[i] == self.c_deck[i]:
                    blacks += 1
                elif input[i] in self.c_deck:
                    whites += 1
            
            return (blacks,whites)

    def check_all(self, moves, response):
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
        scores = []
        for i in moves:
            scores.append(sum(i))
        
        return scores
    
    def algo(self):
        self.start_time = time.time()
        self.colours = [i for i in range(1, 7)]
        print("Jesteś w trybie Komputer vs Komputer")
        self.c_deck = (self.randomize('cpu'))
        print("CPU: ",self.c_deck)
        moves = list(itertools.product(self.colours, repeat=4))
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
                self.p_deck = moves[scores.index(min(scores))]
                moves.remove(self.p_deck)
                print(f"Player Choice: {self.p_deck}") 
            else:
                print(f"Wygrałeś w {rounds} ruchach | Czas: {time.time() - self.start_time}")
                self.gameEnd = True
                exit()

game = Mastermind()