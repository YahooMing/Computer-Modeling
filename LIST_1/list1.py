import random as rd
import matplotlib.pyplot as pt

board1 = [0] * 40
board2 = [0] * 40
board3 = [0] * 40
board4 = [0] * 40

n1=100
n2=1000000

def dice_throw(how_much, flag, board):
    place = 0
    for i in range(how_much):
        dice1 = rd.randint(1,6)
        dice2 = rd.randint(1,6)
        sum = place + dice1 + dice2
        if ( sum > 39):
            place = sum - 40
        elif ( flag and sum == 29 ):
            board[sum]= board[sum] + 1
            place = 10
        else:
            place = sum
        board[place]= board[place] + 1

    in_percente(board, how_much)

def draw_plots(titles, boards):
    fig, axs = pt.subplots(2, 2, figsize=(12, 10))
    indices = list(range(40))

    for ax, title, board in zip(axs.flatten(), titles, boards):
        ax.bar(indices, board, edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel('Pole')
        ax.set_ylabel('Szansa')

    pt.tight_layout()
    pt.show()

def in_percente(board, n):
    for i in range(len(board)):
        board[i] = board[i] / n


dice_throw(n1, False, board1)
dice_throw(n1, True, board2)
dice_throw(n2, False, board3)
dice_throw(n2, True, board4)


titles = ["100 rzutów bez więzienia","100 rzutów z więzieniem","1mln rzutów bez więzienia","1mln rzutów z więzeniem"]
boards = [board1, board2, board3, board4]
draw_plots(titles, boards)
