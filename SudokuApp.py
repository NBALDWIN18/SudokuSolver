from Sudoku import Board
from tkinter import *

window = Tk()
 
window.title("Sudoku")

board = Board()

boxes = []
nodes = []
colors = ['red','orange','yellow','green','blue','purple','pink','brown','black']

f = Frame(window, bg = "black", width = 500, height = 500)
f.pack(side=LEFT, expand = 1)

def NodeClicked(index):
    print( "Node " + str(index) + "clicked" )

for i in range (9):
    boxes.append(Frame(f, bg=colors[i],width=150,height=150))
    #boxes[i].pack(side=LEFT, expand = 1)
    boxes[i].grid(row=i//3,column=i%3, padx=2, pady=2)

for i in range (81):
    nodes.append(Text(boxes[(i//3)%3 + (i//27)*3],width=4,height=2))
    nodes[i].tag_configure("center", justify='center')
    nodes[i].insert(END,board.GetNode(i))
    nodes[i].tag_add("center", "1.0", "end")
    nodes[i].grid(row=i//9,column=i%9)
 
window.mainloop()