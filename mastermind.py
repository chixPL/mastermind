"""
Implementacja Mastermind w Pythonie
Jakub Rutkowski (chixPL) 2023

Po uruchomieniu programu użytkownik może wybrać jeden z dwóch możliwych trybów.
"Tryb gry" jak najwierniej odwzorowuje grę planszową i jest to tryb, w którym ludzki gracz gra przeciwko komputerowi.

Zasady:
- 4 kolumny
- 4 pola sprawdzające
- 10 prób
- 8 kolorów (red, green, blue, yellow, violet, olive, pink, teal)
- 2 kolory sprawdzające (white, blacK)
- gra z komputerem

Tryb algorytmu używa uproszczonej wersji gry z zasadami zdefiniowanymi w oryginalnym artykule Knutha. Źródło jest dostępne w README.

Zasady trybu algorytmicznego:
- 4 kolumny
- 4 pola sprawdzające (czarne i białe)
- Nieograniczona liczba prób
- 6 kolorów, uproszczonych jako liczby
- 2 kolory sprawdzające (white, blacK)
- Komputer gra przeciwko sobie za cel mając osiągnięcie jak najmniejszej ilości tur do odgadnięcia kodu

Stworzone przy użyciu Pythona 3.10.6 i biblioteki standardowej.
"""
import random
import itertools
import time

class Mastermind:

    def __init__(self) -> None:
        self.c_deck = [] # Talia komputera
        self.gameEnd = False # Zmienna końca gry
        self.turns = 0 # Licznik tur
        self.tryb = '' #  Tryb gry lub algorytmu
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
            self.tryb = input() # Wybór trybu przez użytkownika (a=gra, b=algorytm)
            if self.tryb not in ['a','b']:
                print("Źle wybrałeś tryb!")
            else:
                break

        if self.tryb == 'a':
            self.colours = ['R','G','B','Y','V','O','P','T'] 
            self.create_deck('game')
            while(self.gameEnd == False):
                if(self.turns == 10):
                    print("Przegrałeś.")
                    exit()
                else:
                    self.player_turn()
        else:
            self.create_deck('cpu')
            self.algo()

    def randomize(self, mode):
        deck = []
        if mode == 'game':
            elems = self.colours #  Użyj tablicy kolorów zgodnie z zasadami gry planszowej
            for i in range(4):
                colour = random.choice(elems)
                deck.append(colour)
                elems.remove(colour)

            return deck
        else:
            elems = []
            for i in range(1, 6): #  Użyj liczb dla lepszej przejrzystości matematycznej w trybie algorytmu
                elems.append(i)
            for i in range(4):
                colour = random.choice(elems)
                deck.append(colour)
                elems.remove(colour)
            return tuple(deck)


    def create_deck(self, mode):
        self.c_deck = self.randomize(mode)
        print(self.c_deck)

    def player_turn(self): #  Pętla wprowadzania danych przez użytkownika
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
        """
        Sprawdzenie każdej kulki:
        Jeśli kolor i indeks pasują, to jest to czarna kulka.
        Jeśli tylko kolor pasuje (jest w tablicy c_deck, ale w złym miejscu), to jest to biała kulka.
        Jeśli nie ma żadnej kulki o wybranym kolorze, zwróć pustego stringa. 
        """
        if self.tryb == 'a':
            for i in range(0, len(input)):
                if input[i] == self.c_deck[i]:
                    self.answers.append('K')
                elif input[i] in self.c_deck:
                    self.answers.append('W')
                else:
                    self.answers.append('')
            if self.answers == ['K', 'K', 'K', 'K']: #  Jeśli wszystkie kołki w talii kontrolnej są czarne, zakończ grę
                self.gameEnd = True
                print("Wygrałeś!")
                exit()
            else:
                self.answers = sorted(self.answers, key=lambda x: (x == "", x.lower()))
                """
                ^^^ To używa manipulacji kodem ASCII do sortowania, ale żeby puste stringi były na końcu. 
                Dzięki temu odpowiedź jest bardziej czytelna dla użytkownika końcowego.
                """
                print(self.answers)
        else:
            blacks = 0
            whites = 0
            for i in range(0, len(input)):
                if input[i] == self.c_deck[i]:
                    blacks += 1
                elif input[i] in self.c_deck:
                    whites += 1
                # W trybie algorytmu puste kulki nie są liczone, ponieważ istnieją tylko dla wygody użytkowników.
            
            return (blacks,whites) # Kolory są reprezentowane przez liczby dla lepszej matematycznej przejrzystości. 

    def check_all(self, moves, response):
        """
        Tylko w trybie algorytmu.
        Sprawdza całą tablicę ruchów względem odpowiedzi kodera, aby wyeliminować niemożliwe ruchy.
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
        Tylko w trybie algorytmu.
        Knuth stosuje konwencję wyboru ruchu o najmniejszej wartości liczbowej, np. 2345 jest niższe niż 3456.
        Dlatego zawsze wybierany jest ruch z najniższą sumą wartości.
        """
        scores = []
        for i in moves:
            scores.append(sum(i))
        
        return scores
    
    def algo(self):
        self.start_time = time.time()
        self.colours = [i for i in range(1, 7)]
        print("Jesteś w trybie Komputer vs Komputer")
        self.c_deck = (self.randomize('cpu')) #  Stwórz talię komputerową w trybie uproszczonego algorytmu
        print("CPU: ",self.c_deck)
        moves = list(itertools.product(self.colours, repeat=4)) #  W znormalizowanej przez Knutha wersji gry możliwe jest 1296 (6^4) kodów.
        self.p_deck = (1, 1, 2, 2) # Zaczynamy od 1, 1, 2, 2 zgodnie z zasadami metody Knutha.

        rounds = 0

        while(self.gameEnd != True):
            result = self.check(self.p_deck)
            rounds += 1
            if(result != (4,0)):  # Jeśli wszystkie kołki w talii kontrolnej są czarne, zakończ grę
                moves = self.check_all(moves, result)
                print("-----------------")
                print(f"Komputer: {self.c_deck}")
                print(f"Ruchy: {moves}")
                scores = self.score(moves)
                self.p_deck = moves[scores.index(min(scores))] #  Określa następny ruch, który ma być sprawdzony z koderem
                moves.remove(self.p_deck)
                print(f"Wybór gracza: {self.p_deck}") 
            else:
                print(f"Wygrałeś w {rounds} ruchach | Czas: {time.time() - self.start_time}")
                self.gameEnd = True
                exit()

game = Mastermind() #  Rozpocznij grę