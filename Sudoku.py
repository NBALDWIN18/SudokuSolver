'''
Add comments

'''

class Board:
    __slots__: ['rows','cols','boxes']

    class Node():
        def __init__(self, row, col, box):
            #Index for each container
            self.row = row
            self.col = col
            self.box = box
            self.start = False

            #Value for the node
            self.value = 0

        def __str__(self):
            return str(self.value)

        def __repr__(self):
            return str(self.value)

        def __eq__(self, other):
            if isinstance(other, int):
                if self.value == other:
                    return True

        def __add__(self, other):
            return self.value + other.value

        def __radd__(self, other):
            return self.value + other


    def __init__(self):
        self.rows = [[],[],[],[],[],[],[],[],[]]
        self.cols = [[],[],[],[],[],[],[],[],[]]
        self.boxes = [[],[],[],[],[],[],[],[],[]]
        
        #Sum of all values, used to find win
        self.sum = 0

        for i in range(81):
            newNode = self.Node(i//9, i%9, (i//3)%3 + (i//27)*3)
            self.rows[i//9].append(newNode)
            self.cols[i%9].append(newNode)
            self.boxes[(i//3)%3 + (i//27)*3].append(newNode)

    def __str__(self):
        final = ''
        for row in self.rows:
            line = ''
            for node in row:
                line += str(node.value) + ' - '
            final += line[:-2] + '\n'
        return final

    def IsValid(self, row, col, value):
        if(value in self.rows[row]):
            return False
        elif(value in self.cols[col]):
            return False
        elif(value in self.boxes[self.rows[row][col].box]):
            return False
        return True

    def Insert(self, row, col, value, start=False):
        if(self.IsValid(row,col,value)):
            self.rows[row][col].value = value
            self.rows[row][col].start = start
            self.sum += value
            return True
        else:
            return False

    def Remove(self, row, col):
        self.sum -= self.rows[row][col].value
        self.rows[row][col].value = 0

    def CheckWin(self):
        total = 0
        for index in range (9):
            total += sum(self.rows[index])
            total += sum(self.cols[index])
            total += sum(self.boxes[index])
        return total == 1215

    def ApplyTemplate(self, diff):
        if diff == "E":
            fp = open("SudokuEasy.txt")
        elif diff == 'M':
            fp = open("SudokuMedium.txt")
        elif diff == 'H':
            fp = open("SudokuHard.txt")
        elif diff == 'C':
            fp = open(input('Enter file name: '))
        else:
            print("INVALID INPUT")
            return
        lines = fp.readlines()
        for line in lines:
            vals = line.split()
            self.Insert(int(vals[0]),int(vals[1]),int(vals[2]), True)

    def GetNode(self, index):
        try:
            return self.rows[index//9][index%9]
        except IndexError:
            print(index)

    def Fix(self, index):
        start = index
        val = 1
        while True:
            while val < 10:
                insert = self.Insert(index//9,index%9, val)
                if insert:
                    if index == start:
                        return
                    index+=1
                    while self.GetNode(index).start:
                        index += 1
                    val = 0
                val +=1
            self.GetNode(index).value = 0
            index -= 1
            while self.GetNode(index).start:
                index -= 1
            val = self.GetNode(index).value
        
    def Solve(self):
        for index in range (81):
            if self.GetNode(index).start:
                continue
            for value in range (1,10):
                insert = self.Insert(index//9,index%9, value)
                if insert:
                    break
            if not insert:
                self.Fix(index)