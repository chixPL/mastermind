# Mastermind
Implementacja gry planszowej Mastermind z trybem gry przeciwko komputerowi oraz algorytmem Knutha.

## Zasady gry
Jeden z graczy przyjmuje rolę kodera (code maker), a drugi rolę łamacza kodów lub Masterminda.
Koder ma za zadanie ułożyć z 8 różnokolorowych kulek sekwencję 4 kulek, a następnie odpowiedzieć łamaczowi kodu określoną sekwencją kulek.
Czarna kulka oznacza, że kulka o danym kolorze została umieszczona we właściwym miejscu.
Biała kulka oznacza, że kolorowy kołek istnieje w kodzie, ale jest w złym miejscu.
Celem jest określenie poprawnego kodu. Jeśli uda się to zrobić w ciągu określonej liczby prób, Mastermind wygrywa.

Możesz zagrać w prostą implementację gry w HTML5 [tutaj.](https://webgamesonline.com/mastermind/)

## Przegląd programu

Program posiada dwa różne tryby: tryb gry i tryb algorytmu. Zasady dla obu są podane poniżej.

**Zasady trybu gry**:
- Kod do ustalenia składa się z 4 kulek.
- 4 miejsca na kulki sprawdzające - czarne i białe
- 10 prób
- 8 kolorów (czerwony, zielony, niebieski, żółty, fioletowy, oliwkowy, różowy, morski).
(info: w programie są oznaczone angielskimi skrótami: red, green, blue, yellow, violet, olive, pink, teal, white, blacK)
- Dwa kolory kulek sprawdzających:
    Czarny (oznaczony literą K) = kulka jest na właściwym miejscu
    Biały (W) = kulka jest w kodzie, ale jest w złym miejscu
- Gra przeciwko komputerowi

**Zasady trybu algorytmu**:
- Kod do ustalenia składa się z 4 kulek.
- 4 miejsca na kulki sprawdzające - czarne i białe
- Nieograniczona liczba prób
- 6 kolorów, zapisanych w postaci liczb
- Dwa kolory kulek sprawdzających:
    Czarny (oznaczony literą K) = kulka jest na właściwym miejscu
    Biały (W) = kulka jest w kodzie, ale jest w złym miejscu
- Komputer gra przeciwko sobie, za cel mając osiągnięcie jak najmniejszej ilości tur do odgadnięcia kodu

*Stworzone w Python 3.10.6 ze standardową biblioteką.*

## Algorytm metody Knutha

Można go przeczytać na Wikipedii [tutaj](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm). Postaram się tutaj przedstawić lepsze wyjaśnienie.
1. Zacznij od 1122 jako początkowej kombinacji.
``python
player_deck = [1, 1, 2, 2]
```
2. Wygeneruj wszystkie możliwe kombinacje poprzez iloczyn kartezjański wartości kolorów.
``python 
moves = list(itertools.product(colors, repeat=4))
```
3. Sprawdź wybraną kombinację z koderem, otrzymując jego odpowiedź składającą się z czarnych i białych kołków.
4. Jeśli odpowiedź kodera to 4,0 (wszystkie czarne kołki), zakończ algorytm.
5. W przeciwnym razie, sprawdź wszystkie możliwe ruchy względem odpowiedzi kodera w 4. Usuń wszystkie ruchy, które nie zwracają tej wartości.
- Przykład:
Poprawna kombinacja to 1234. Dla talii gracza=1122, otrzymujemy odpowiedź 1 czarny kołek i 1 biały kołek. Sprawdzamy wszystkie ruchy i usuwamy te, które nie zwracają 1 czarnego i 1 białego.
6. Używamy algorytmu min max do wyboru następnego ruchu. Knuth stosuje konwencję wyboru ruchu o najmniejszej wartości liczbowej, np. 2345 jest mniejsze niż 3456. Z pozostałych ruchów wybierz ten, który ma minimalną sumę wartości liczbowych.
7. Powtórz czynności od 3.

### Podziękowania dla:
- Donalda Knutha za wymyślenie algorytmu.
- Ilana Schnella za bardziej przejrzyste wyjaśnienie algorytmu [(źródło)](https://github.com/ilanschnell/mastermind)

[^1]: Źródło: http://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf