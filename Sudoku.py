'''
Author: Nolan Baldwin
Background functionality for Sudoku game
'''

#Class representing the Sudoku board
class Board(object):
    __slots__: ['rows','cols','boxes']

    #Class representing a single node (square) on the board
    class Node(object):

        '''
        Node constructor
        :param row: the row number
        :param col: the column number
        :param box: the box number
        '''
        def __init__(self, row, col, box):
            #Index for each container
            self.row = row
            self.col = col
            self.box = box

            #Whether or not the node is given at start
            self.start = False      

            #Value for the node
            self.value = 0

        #Node to string
        def __str__(self):
            return str(self.value)

        #Node representation
        def __repr__(self):
            return str(self.value)

        #Equality comparison
        def __eq__(self, other):

            #If comparing a node to a number
            if isinstance(other, int):
                return self.value == other
            #If comparing two nodes, compare values only
            elif isinstance(other, Board.Node):
                return self.value == other.value

        '''
        def __add__(self, other):
            return self.value + other.value

        def __radd__(self, other):
            return self.value + other
        '''

    #Board constuctor
    def __init__(self):
        #Each container has 9 instances
        self.rows = [[],[],[],[],[],[],[],[],[]]
        self.cols = [[],[],[],[],[],[],[],[],[]]
        self.boxes = [[],[],[],[],[],[],[],[],[]]
        
        #Sum of all values, used to find win
        self.sum = 0

        #Generates 81 nodes and loads them into the containers
        for i in range(81):
            newNode = self.Node(i//9, i%9, (i//3)%3 + (i//27)*3)
            self.rows[i//9].append(newNode)
            self.cols[i%9].append(newNode)
            self.boxes[(i//3)%3 + (i//27)*3].append(newNode)

    #Board to string
    def __str__(self):
        final = ''
        for row in self.rows:
            line = ''
            for node in row:
                line += str(node.value) + ' - '
            final += line[:-2] + '\n'
        return final

    def __eq__(self, other):
        #If comparing two boards, compare the rows container
        if isinstance(other, Board):
            return self.rows == other.rows

    '''
    Checks if value can be inserted at requested location
    :param row: the row number
    :param col: the column number
    :param value: the value to be checked
    :return: if the location is valid for the value
    '''
    def IsValid(self, row, col, value):
        if(value in self.rows[row]):
            return False
        elif(value in self.cols[col]):
            return False
        elif(value in self.boxes[self.rows[row][col].box]):
            return False
        return True

    '''
    Inserts the a value at a location
    :param row: the row number
    :param col: the column number
    :param value: the value to be inserted
    :param start: if the node should be a start node
    :return: if the insertion was successful
    '''
    def Insert(self, row, col, value, start=False):
        if(self.IsValid(row,col,value)):
            self.rows[row][col].value = value
            self.rows[row][col].start = start
            self.sum += value
            return True
        return False

    '''
    Removes a value from the location
    :param row: the row number
    :param col: the column number
    :return: if the removal was successful
    '''
    def Remove(self, row, col):
        #Cannot remove a start node
        if not self.rows[row][col].start:
            self.sum -= self.rows[row][col].value
            self.rows[row][col].value = 0
            return True
        return False

    '''
    Check if the board is correct
    :return: if the board is correct
    '''
    def CheckWin(self):
        total = 0
        for index in range (9):
            #Each should sum to 405
            total += sum(self.rows[index])
            total += sum(self.cols[index])
            total += sum(self.boxes[index])
        return total == 1215

    '''
    Applies a premade board
    :param diff: the selected board by difficulty
    '''
    def ApplyTemplate(self, file):
        #Selects and opens a file
        try:
            fp = open(file)
        except:
            print("FILE ERROR")
            return

        
        #Inserts all the nodes into the board
        lines = fp.readlines()
        for line in lines:
            vals = line.split()
            self.Insert(int(vals[0]),int(vals[1]),int(vals[2]), True)

    '''
    Gets the node at an index 0-80
    :param index: the requested index
    :return: the node at the index
    '''
    def GetNode(self, index):
        try:
            return self.rows[index//9][index%9]
        except IndexError:
            print(index)

    '''
    Iterates backwards adjusting values to fix an error
    :param index: The index where the error occurred
    '''
    def Fix(self, index):
        start = index       #Remember the start index
        val = 1             #The test value to be inserted

        while True:
            while val < 10: #Try values 1-9
                insert = self.Insert(index//9,index%9, val)

                #If the inserted step foward
                if insert:
                    if index == start:  #a number was successfully inserted at start, error fixed
                        return
                    index+=1
                    while self.GetNode(index).start:    #If node is start skip it
                        index += 1
                    val = 0
                val +=1
            self.GetNode(index).value = 0
            index -= 1

            while self.GetNode(index).start:            #If node is start skip it
                index -= 1
            val = self.GetNode(index).value
        
    '''
    Solves the game board
    '''
    def Solve(self):
        for index in range (81):            #Go through each node
            if self.GetNode(index).start:   #If start node, skip it
                continue

            for value in range (1,10):      #Try all values

                insert = self.Insert(index//9,index%9, value)
                if insert:
                    break
            if not insert:                  #If insertion fail, look for error
                self.Fix(index)

        return self