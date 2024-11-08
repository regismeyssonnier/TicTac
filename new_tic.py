import tkinter as tk
from PIL import Image, ImageTk

import random
import sys
import time
import math

MAX_DOUBLE = sys.float_info.max

class Node:

    def __init__(self):
        self.grid = [-1] * 9
        self.n = 0
        self.score = 0
        self.child = []
        self.num = -1
        self.terminal = False
        self.winner = -2
        self.player = 0
        self.parent = None


    def get_State(self):

        g = []
        for i  in range(9):
            g.append(self.grid[i])

        return g

    def get_PossibleCoup(self):
        coup = []
        for i in range(9):
            if self.grid[i] == -1:
                coup.append(i)

        return coup

def get_PossibleCoup(grid):
    coup = []
    for i in range(9):
        if grid[i] == -1:
            coup.append(i)

    return coup

winning_moves = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

def CheckWinorDraw(grid, player):

    win = False
    for i in range(8):
        nb = 0
        for j in range(3):
            if grid[winning_moves[i][j]] == player:
                nb+=1

        if nb == 3:
            return player

    coup = get_PossibleCoup(grid)
    if len(coup) == 0: return -3

    return -2

def CheckWinLoseDraw(grid):

    win = False
    for i in range(8):
        nb = 0
        for j in range(3):
            if grid[winning_moves[i][j]] == 0:
                nb+=1

        if nb == 3:
            return 0

        nb = 0
        for j in range(3):
            if grid[winning_moves[i][j]] == 1:
                nb+=1

        if nb == 3:
            return 1

    coup = get_PossibleCoup(grid)
    if len(coup) == 0: return -3

    return -2


    
class MCTS:

    def __init__(self, player, c):
        self.grid = [-1] * 9
        self.player = player
        self.c = c

    def get_State(self):

        g = []
        for i  in range(9):
            g.append(self.grid[i])

        return g

    def select(self, node : Node) -> Node:

        depth = 0
        while 1:

            #if node.winner != -2:
            #    return node, depth

            if len(node.child) == 0:
                coup = node.get_PossibleCoup()
                if len(coup) != 0:
               
                    for c in coup:
                        n = Node()
                        n.grid = node.get_State()
                        n.num = c
                        n.player = node.player ^ 1
                        n.grid[c] = n.player
                        n.winner = CheckWinorDraw(n.grid, n.player)
                        n.parent = node
                                         
                        node.child.append(n)
                    
                    return node.child[0], depth
                else:
                    return node, depth
            
            else:
                maxscore = -float('inf')
                ind = -1
                for i in range(len(node.child)):
                    stat = 0
                    if node.child[i].n == 0:
                        stat = MAX_DOUBLE
                    else:
                        stat = node.child[i].score / node.child[i].n + self.c * math.sqrt(math.log(node.n) / node.child[i].n)

                    if stat > maxscore:
                        maxscore = stat
                        ind = i

                node = node.child[ind]
                if node.n == 0:
                    return node, depth

            depth += 1



    def rollout(self, node : Node)->int:

        if node.winner != -2:return node.winner
        player = node.player ^1
        state = node.get_State()
        while 1:
            coup = get_PossibleCoup(state)
            #if len(coup) != 0:
            cp = random.randint(0, len(coup)-1)
            state[coup[cp]] = player
            win = CheckWinorDraw(state, player)
            if win != -2: return win
            player = player ^ 1

    def backpropagation(self, node, won):

        par = node

        while par != None:
            par.n+=1
            if won == -3:
                par.score += 1
            elif won == par.player:
                par.score += 1
            #else:
            #    par.score -= 1

            par = par.parent


    def Play(self, sec):

        root = Node()
        root.grid = self.get_State()
        root.player = self.player ^ 1
        #print(root.grid)

        end = time.perf_counter() + sec
        while time.perf_counter() < end:
            leaf, d = self.select(root)
            #print('depth=', d)
            won = self.rollout(leaf)
            self.backpropagation(leaf, won)

        num = 0
        maxscore = -float('inf')
        for i in range(len(root.child)):

            if root.child[i].winner == self.player:
                print('return winner')
                return root.child[i].num
            
            score = root.child[i].n

            print(i, score)
            if score  > maxscore:
                maxscore = score
                num = root.child[i].num

        return num;







class TicTac:

    def __init__(self):
        self.cross = []
        self.circle = []
        self.ind_c = 0
        self.ind_cr = 0
        self.display_c = [False]*9
        self.display_cnum = [0]*9
        self.display_cr = [False]*9
        self.display_crnum = [0]*9
        self.grid = [-1] * 9
        self.p1 = MCTS(0, math.sqrt(2))
        self.p2 = MCTS(1, 0.6)
        self.startp = 0
        self.player = 0
        self.label = []
        self.score_p1 = 0
        self.score_p2 = 0

      
        image = Image.open("cross.png")
        self.cross.append(ImageTk.PhotoImage(image))

        image = Image.open("circle.png")
        self.circle.append(ImageTk.PhotoImage(image))

    def play(self, fen, num, type):

        if type == 'circle':
            self.display_c[self.ind_c] = True
            self.display_cnum[self.ind_c] = num
            self.ind_c+=1
            

        if type == 'cross':
            self.display_cr[self.ind_cr] = True
            self.display_crnum[self.ind_cr] = num
            self.ind_cr+=1

    def get_PossibleCoup(self):
        coup = []
        for i in range(9):
            if self.grid[i] == -1:
                coup.append(i)

        return coup

    def get_Grid(self):

        g = []
        for i  in range(9):
            g.append(self.grid[i])

        return g

    def Clear_game(self):
        self.display_c = [False]*9
        self.display_cnum = [0]*9
        self.display_cr = [False]*9
        self.display_crnum = [0]*9
        self.grid = [-1] * 9
        self.ind_c = 0
        self.ind_cr = 0
        for l in self.label:
            l.destroy()

    def Display(self, fen):

        global label_p1
        global label_p2
        global TURN

        won = CheckWinorDraw(self.grid, self.player)
        print(won)
        if won == -2:
            if self.player == 0:
                self.p1.grid = self.get_Grid()
                num = 0
                #if TURN == 0:
                #    coup = self.get_PossibleCoup()
                #    num = coup[random.randint(0, len(coup)-1)]
                #else:
                num = self.p1.Play(0.1)
                self.grid[num] = 0
                print(num, 'p1=', self.grid)
                self.play(fen, num, 'circle')
                self.player = self.player^1
            else:
                self.p2.grid = self.get_Grid()
                num = 0
                #if TURN == 0:
                #    coup = self.get_PossibleCoup()
                #    num = coup[random.randint(0, len(coup)-1)]
                #else:
                num = self.p2.Play(0.1)
                self.grid[num] = 1
                print(num, 'p2=', self.grid)
                self.play(fen, num, 'cross')
                self.player = self.player^1

            TURN += 1

        if won == 0:
            self.score_p1 += 1
        elif won == 1:
            self.score_p2 += 1

        label_p1.config(text='P1=' + str(self.score_p1))
        label_p2.config(text='P2=' + str(self.score_p2))

        if won != -2:
            self.Clear_game()
            self.p1 = MCTS(0, math.sqrt(2))
            self.p2 = MCTS(1, 0.6)
            self.startp = self.startp ^ 1
            self.player = self.startp
            print("------------------------------------")
            TURN = 0
        

        
      

        for i in range(9):
            if self.display_c[i] :
                label = 0
                if self.display_cnum[i] == 0:
                    label = tk.Label(fen, image=self.circle[0], bg = "blue")
                    label.place(x=150, y=50)
                if self.display_cnum[i] == 1:
                    label = tk.Label(fen, image=self.circle[0], bg = "blue")
                    label.place(x=330, y=50)

                if self.display_cnum[i] == 2:
                    label = tk.Label(fen, image=self.circle[0], bg = "blue")
                    label.place(x=515, y=50)

                if self.display_cnum[i] == 3:
                    label = tk.Label(fen, image=self.circle[0], bg = "blue")
                    label.place(x=150, y=225)

                if self.display_cnum[i] == 4:
                    label = tk.Label(fen, image=self.circle[0], bg = "blue")
                    label.place(x=330, y=225)

                if self.display_cnum[i] == 5:
                    label = tk.Label(fen, image=self.circle[0], bg = "blue")
                    label.place(x=515, y=225)

                if self.display_cnum[i] == 6:
                    label = tk.Label(fen, image=self.circle[0], bg = "blue")
                    label.place(x=150, y=400)

                if self.display_cnum[i] == 7:
                    label = tk.Label(fen, image=self.circle[0], bg = "blue")
                    label.place(x=330, y=400)

                if self.display_cnum[i] == 8:
                    label = tk.Label(fen, image=self.circle[0], bg = "blue")
                    label.place(x=515, y=400)

                self.label.append(label)

            if self.display_cr[i] :
                if self.display_crnum[i] == 0:
                    label = tk.Label(fen, image=self.cross[0], bg = "red")
                    label.place(x=150, y=50)
                if self.display_crnum[i] == 1:
                    label = tk.Label(fen, image=self.cross[0], bg = "red")
                    label.place(x=330, y=50)

                if self.display_crnum[i] == 2:
                    label = tk.Label(fen, image=self.cross[0], bg = "red")
                    label.place(x=515, y=50)

                if self.display_crnum[i] == 3:
                    label = tk.Label(fen, image=self.cross[0], bg = "red")
                    label.place(x=150, y=225)

                if self.display_crnum[i] == 4:
                    label = tk.Label(fen, image=self.cross[0], bg = "red")
                    label.place(x=330, y=225)

                if self.display_crnum[i] == 5:
                    label = tk.Label(fen, image=self.cross[0], bg = "red")
                    label.place(x=515, y=225)

                if self.display_crnum[i] == 6:
                    label = tk.Label(fen, image=self.cross[0], bg = "red")
                    label.place(x=150, y=400)

                if self.display_crnum[i] == 7:
                    label = tk.Label(fen, image=self.cross[0], bg = "red")
                    label.place(x=330, y=400)

                if self.display_crnum[i] == 8:
                    label = tk.Label(fen, image=self.cross[0], bg = "red")
                    label.place(x=515, y=400)

                self.label.append(label)

        fen.after(10, self.Display, fen)



# Créer la fenêtre principale
root = tk.Tk()
root.title("Tic Tac")

# Charger l'image (assurez-vous que le fichier image.png existe dans le même dossier)
image_path = "back.png"
image = Image.open(image_path)
back_photo = ImageTk.PhotoImage(image)

# Créer un label pour afficher l'image et le positionner
label = tk.Label(root, image=back_photo)
label.place(x=0, y=0)  # Coordonnées (x, y) pour placer l'image dans la fenêtre

# Dimensionner la fenêtre en fonction de l'image (optionnel)
root.geometry(f"{image.width}x{image.height}")

label_p1 = tk.Label(root, text='P1=-1', bg = "blue",  font=("Arial", 40))
label_p1.place(x=0, y=0)
label_p2 = tk.Label(root, text='P2=-1', bg = "red",  font=("Arial", 40))
label_p2.place(x=0, y=75)

tic = TicTac()

TURN = 0

tic.Display(root)

# Lancer la boucle principale de l'application
root.mainloop()


"""
tic.play(root, 0, 'circle')
tic.play(root, 1, 'circle')
tic.play(root, 2, 'circle')
tic.play(root, 3, 'circle')
tic.play(root, 4, 'circle')
tic.play(root, 5, 'circle')
tic.play(root, 6, 'circle')
tic.play(root, 7, 'circle')
tic.play(root, 8, 'circle')


tic.play(root, 0, 'cross')
tic.play(root, 1, 'cross')
tic.play(root, 2, 'cross')
tic.play(root, 3, 'cross')
tic.play(root, 4, 'cross')
tic.play(root, 5, 'cross')
tic.play(root, 6, 'cross')
tic.play(root, 7, 'cross')
tic.play(root, 8, 'cross')
"""