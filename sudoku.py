#!/usr/bin/python
import math
import sys
import time
import random
import signal

FAILURE = 1
UNASSIGNED = 0


def handler(signum, frame):
    print("Forever is over!")
    raise Exception("end of time")

class Variable:

    def __init__(self,row=0,column=0,value=UNASSIGNED):
        self.row = row
        self.column = column
        self.value = value
        self.br = int(row/3)*3
        self.bc = int(column/3)*3

    def __eq__(self, other):
        if self.row == other.row and self.column == other.column:
            return True
        return False

    def constraining(self,empty_nodes):
        counter = 0
        for i in range(0,len(empty_nodes)):
            temp = empty_nodes[i]
            # check for variables in same row or same column
            if (temp.row == self.row) != (temp.column == self.column):
                counter += 1
            #check remaining four variables in the box
            elif temp.br == self.br and temp.bc == self.bc and (temp.row != self.row or temp.column != self.column):
                counter += 1
        return counter



class Sudoku:

    def __init__(self):
        self.grid = []
        self.num_nodes = 0
        for i in range(0,9):
            self.grid.append([])
            for j in range(0,9):
                temp = Variable(i,j,UNASSIGNED)
                self.grid[i].append(temp)

    def grid_add(self,var,val):
        self.grid[var.row][var.column].value = val
        var.value = val
        return 0

    def grid_remove(self,var):
        self.grid[var.row][var.column].value = UNASSIGNED
        var.value = UNASSIGNED


    def __str__(self):
        ret = ""
        for i in range(0,9):
            for j in range(0,9):
                ret += str(self.grid[i][j].value)
            ret += "\n"
        return ret

    def is_consistent(self, var, val):
        r = var.row
        c = var.column
        # check row
        for j in range(0, 9):
            if self.grid[r][j].value == val:
                return False
        # check column
        for i in range(0, 9):
            if self.grid[i][c].value == val:
                return False
        # check box: find which box
        for i in range(int(var.br), int(var.br + 3)):
            for j in range(int(var.bc), int(var.bc + 3)):
                if self.grid[i][j].value == val:
                    return False
        return True

    def get_empty(self):
        empty = []
        for i in range(0,9):
            for j in range(0,9):
               if self.grid[i][j].value == UNASSIGNED:
                  empty.append(self.grid[i][j])
        return empty

    def order_domain(self,method):
        domain = []
        [domain.append(list(range(1, 10))) for i in range(81)]
        if method != "B":
            for i in range(0, 9):
                for j in range(0, 9):
                    if self.grid[i][j].value != UNASSIGNED:
                        # remove the value from the constrained squares
                        var = self.grid[i][j]
                        domain = remove_values(var, domain)
        return domain


def remove_values(var, old_domain):
    value = var.value
    row = var.row
    column = var.column
    br = var.br
    bc = var.bc
    old_domain[column + row * 9] = [0]
    for i in range(0, 9):
        if value in old_domain[row * 9 + i]:
            old_domain[row * 9 + i].remove(value)

    for j in range(0, 9):
        if value in old_domain[column + 9 * j]:
            old_domain[column + 9 * j].remove(value)


    for i in range(3):
        for j in range(3):
            if value in old_domain[bc + j + (br + i) * 9]:
                old_domain[bc + j + (br + i) * 9].remove(value)
    return old_domain


def forward_checking(all_domain,var,val):
    row = var.row
    column = var.column
    br = var.br
    bc = var.bc
    for i in range(0,9):
        temp = all_domain[row * 9 + i]
        if i != column and (val in temp) and (len(temp) == 1):
            return 0
    for j in range(0,9):
        temp = all_domain[column + 9 * j]
        if j != row and (val in temp) and (len(temp) == 1):
            return 0

    for i in range(3):
        for j in range(3):
            temp =  all_domain[bc + j + (br + i) * 9]
            if br+i==row and bc+j==column:
                continue
            if (val in temp) and (len(temp) == 1):
                return 0

    return 1

def select_unassigned(all_domain,empty_nodes,method):
    result = empty_nodes[0]
    if method != "B+FC+H":
        counter = random.randint(0, len(empty_nodes) - 1)
        result = empty_nodes[counter]
        return result
    else:
        min_domain = 9
        for i in range(0,len(empty_nodes)):
                #search for var with min domain
                temp = empty_nodes[i]
                row = temp.row
                column = temp.column
                if len(all_domain[row*9+column]) < min_domain:
                    min_domain = len(all_domain[row*9+column])
                    result = temp
                elif len(all_domain[row*9+column]) == min_domain:
                    #most constraining variable
                    if result.constraining(empty_nodes) < temp.constraining(empty_nodes):
                        min_domain = len(all_domain[row * 9 + column])
                        rint = random.randint(1,2)
                        if rint == 1:
                            result = temp
        return result


def get_lcv(all_domain,var,val):
    row = var.row
    column = var.column
    bc = var.bc
    br = var.br
    lcv = 0

    for i in range(0, 9):
        temp = all_domain[row * 9 + i]
        if i != column and (val in temp):
            if len(temp) == 1:
                return -1
            lcv += 1

    for j in range(0, 9):
        temp = all_domain[column + 9 * j]
        if j != row and (val in temp):
            if len(temp) == 1:
                return -1
            lcv += 1

    for i in range(3):
        for j in range(3):
            temp = all_domain[bc + j + (br + i) * 9]
            if br + i == row and bc + j == column:
                continue
            if val in temp:
                if len(temp) == 1:
                    return -1
                lcv += 1
    return lcv

def compare_with_ties(x, y):
    if x < y:
        return -1
    elif x > y:
        return 1
    else:
        return random.randint(0, 1) * 2 - 1

def backtracking_search(assignment,method):
    return recursive_backtracking(assignment,method)


def recursive_backtracking(assignment,method):
    assignment.num_nodes += 1
    empty_nodes = assignment.get_empty()
    if len(empty_nodes) == 0:
        return assignment
    all_domain = assignment.order_domain(method)
    var = select_unassigned(all_domain,empty_nodes,method)
    domain = all_domain[var.column+var.row*9]
    if method != "B+FC+H":
        random.shuffle(domain)
    else:
        lcv_list = []
        for val in domain:
            if get_lcv(all_domain,var,val) == -1:
                domain.remove(val)
            else:
                lcv_list.append(get_lcv(all_domain,var,val))
        domain = [i[0] for i in sorted(zip(domain,lcv_list), key=lambda l: l[1], reverse=False)]
    for val in domain:
        if method == "B+FC+H" or (method == "B+FC" and forward_checking(all_domain,var,val)) or (method=="B" and assignment.is_consistent(var,val)):
            assignment.grid_add(var,val)
            result = recursive_backtracking(assignment,method)
            if result != FAILURE:
                return result
            assignment.grid_remove(var)
    return FAILURE


def read_file(name,method):
    initial = True
    sudoku_list = []
    with open(name) as f:
        rawdata = f.readlines()
    rawdata = [x.strip() for x in rawdata]

    for raw_sudoku in rawdata:
        raw_sudoku = str(raw_sudoku)
        counter = 0
        new_sudoku = Sudoku()
        for i in range(0,9):
            for j in range(0,9):
                if raw_sudoku[counter] != '.':
                    new_node = Variable(i,j)
                    node_value = int(raw_sudoku[counter])
                    new_sudoku.grid_add(new_node,node_value)
                counter += 1
        sudoku_list.append(new_sudoku)
    return sudoku_list


def writeSudokuFile(fileName, sudokuList):
    """
    Writes a list of sudoku instances to the given file.
    `fileName` pathname of the file to write to.
    """

    if len(sudokuList) > 0:
        f = open(fileName, "w")
        f.write(str(sudokuList[0]))

    f.close()


def main():
    for i in range(0,10):
        signal.signal(signal.SIGALRM, handler)
        sudokuList = read_file("source","B+FC+H")
        sudokuInstance = sudokuList[0]
        initTime = time.time()
        signal.alarm(1000)
        try:
            result = backtracking_search(sudokuInstance,"B+FC+H")
            if result == FAILURE:
                print("FAILURE!")
        except Exception:
            continue
        duration = time.time() - initTime
        num = sudokuInstance.num_nodes
        print("Time: " + str(duration) + ", number of nodes: " + str(num))
        writeSudokuFile("out.txt", sudokuList)


main()
