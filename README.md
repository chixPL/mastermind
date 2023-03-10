# Mastermind
Mastermind board game implementation in Python with Player vs CPU mode and Knuth method algorithm [(read here)](https://github.com/chixPL/mastermind#knuths-method-algorithm)[^1].

*🇵🇱️ The Polish version is available [here.](https://github.com/chixPL/mastermind/tree/polish)*

## Game rules
One player assumes the role of code-maker, while another the role of code-breaker or Mastermind.
The code-maker's role is to set an 4-peg sequence out of 8 differently colored pegs and then respond to the code-breaker with a specific sequence of pegs.
A black peg denotes that the correctly colored peg has been placed in the right place.
A white peg denotes that the colored peg exists in the code but is in the wrong place.
The goal is to determine the correct code. If done in under an arbitrary amount of tries, the Mastermind wins.

You can play a simple HTML5 implementation of the game [here.](https://webgamesonline.com/mastermind/)

## Program overview

The program has two different modes: game mode and algorithm mode. The rules for both are listed below.

**Game mode rules**:
- 4-peg code to determine
- 4 result pegs (black and white)
- 10 tries
- 8 colours (red, green, blue, yellow, violet, olive, pink, teal)
- Two result colors:
    Black (denoted with K) = The peg is in the correct place
    White (W) = The peg is in the code but is in the wrong place
- Game against a computer

**Algorithm mode rules**:
- 4-peg code to determine
- 4 result pegs (black and white)
- Unlimited number of tries
- 6 colours, simplified as numbers
- Two result colors:
    Black (denoted with K) = The peg is in the correct place
    White (W) = The peg is in the code but is in the wrong place
- Computer plays against itself with the goal of minimizing required turns

*Created with Python 3.10.6 and the standard library.*

## Knuth's method algorithm

You can read it on Wikipedia [here.](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm). I'll try to provide a better explanation.
1. Start with 1122 as the initial combination.
```python 
player_deck = [1, 1, 2, 2]
```
2. Generate the possible moveset through the cartesian product of color values.
```python 
moves = list(itertools.product(colours, repeat=4))
```
3. Check the set combination against the code maker, making note of his response of black and white pegs.
4. If the code maker's response is 4,0 (all black pegs), terminate algorithm.
5. Else, check all possible moves against the code maker's response in 4. Remove all moves that don't return that value.
- Example:
The correct combination is 1234. For player deck=1122, we get a response of 1 black peg and 1 white peg. We check all moves, and those that don't return 1 black and 1 white are removed.
6. Use the min max algorithm to select the next move. Knuth follows the convention of choosing the guess with the least numeric value; e.g., 2345 is lower than 3456. Out of the remaining moveset choose the one with the minimum sum of the numerical values.
7. Repeat from 3.

### Credits:
- Donald Knuth for coming up with the algorithm.
- Ilan Schnell for a more coherent explanation of the algorithm [(source)](https://github.com/ilanschnell/mastermind)

[^1]: Adapted from: http://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf