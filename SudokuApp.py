from Sudoku import Board
from tkinter import *
from tkinter.filedialog import askopenfilename

class App(object):

    def OpenPuzzle(self):
        filename = askopenfilename()
        self.board.ApplyTemplate(filename)
        self.UpdateNodes()

    def Solve(self):
        self.board.Solve()
        self.UpdateNodes()

    def UpdateNodes(self):
        for i in range (81):
            self.nodes[i].config(text=self.board.GetNode(i))

    def __init__(self):
        self.kp = ''
        self.lastNode = None
        self.boxes = []
        self.nodes = []
        self.index = -1
        self.board = Board()
        colors = ['red','orange','yellow','green','blue','purple','pink','brown','black']

        window = Tk()
        window.title("Sudoku")
        window.bind_all("<Key>",self.keyPress)

        menu = Menu(window)
        menu.add_command(label="Open", command= lambda:self.OpenPuzzle())
        menu.add_command(label="Solve", command= lambda:self.Solve())
        window.config(menu=menu)

        f = Frame(window, bg = "black", width = 500, height = 500)
        f.pack(side=LEFT, expand = 1)

        for i in range (9):
            self.boxes.append(Frame(f, bg=colors[i],width=150,height=150))
            self.boxes[i].grid(row=i//3,column=i%3, padx=2, pady=2)

        for i in range (81):
            self.nodes.append(Button(self.boxes[(i//3)%3 + (i//27)*3],width=2,text=self.board.GetNode(i),command=lambda i=i: self.NodeClicked(self.nodes[i],i)))
            self.nodes[i].grid(row=i//9,column=i%9)

        window.mainloop()

    def keyPress(self, event):
        digs = ['1','2','3','4','5','6','7','8','9']
        if str(event.keysym) in digs:
            self.lastNode.config(text=event.keysym)
            if not self.board.Insert(self.index//9, self.index%9,int(event.keysym)):
                self.lastNode.config(bg='red')

    def NodeClicked(self,  node, index):
        if self.lastNode is not None:
            self.lastNode.config(relief=RAISED)
            self.lastNode.config(bg='white')
        self.lastNode = node
        node.config(relief=SUNKEN)
        self.index = index

app = App()