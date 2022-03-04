from ctypes.wintypes import CHAR
from msvcrt import getch
import colorama
from colorama import Fore, Back, Style
import random
import copy

class Board:

    def __init__(self, dimension_in: int):
            colorama.init()
            self.dimension = dimension_in
            self.boardArray = [[0] * dimension_in for x in range(dimension_in)]

            """boardsave used if playing on powerups mode"""
            self.boardSave = []

    def getMove(self, special: bool) -> str:
        valid = False
        while not valid:
            if not special:
                print("Move (arrow keys): ", end = "")
            else:
                print("Move (arrow keys or powerup): ", end = "")
            key = ord(getch())
            print("\n")
            if key == 224:
                valid = True
                key = ord(getch())
                if key == 80:
                    return "down"
                elif key == 75:
                    return "left"
                elif key == 77:
                    return "right"
                elif key == 72:
                    return "up"
                else:
                    valid = False
            if special:
                if key == 113:
                    return "b1"
                if key == 119:
                    return "b2"
                if key == 101:
                    return "b3"
                if key == 122:
                    return "u1"
                if key == 120:
                    return "u2"
                if key == 99:
                    return "u3"
    
    def setMove(self, move_in: str):
        self.smash(move_in)
        self.join(move_in)

    def spawn(self):
        empty = []
        for x in range(self.dimension):
            for y in range(self.dimension):
                if self.boardArray[x][y] == 0:
                    empty.append((x,y))
        if len(empty) == 0:
            return
        coord = random.choice(empty)
        self.boardArray[coord[0]][coord[1]] = random.choice([2, 4])

    def scramble(self):
        boardList = []
        for x in self.boardArray:
            boardList += x
        random.shuffle(boardList)
        self.boardArray = [boardList[i:i + self.dimension] for i in range(0, len(boardList), self.dimension)]

    def saveBoard(self):
        if len(self.boardSave) == 10:
            self.boardSave.pop(0)
        self.boardSave.append(copy.deepcopy(self.boardArray))
    
    def lifeSaver(self):
        self.boardArray = self.boardSave[0]

    def randomDoubler(self):
        empty = []
        for x in range(self.dimension):
            for y in range(self.dimension):
                if self.boardArray[x][y] != 0 and self.boardArray[x][y] < 1024:
                    empty.append((x,y))
        for x in empty:
            token = random.randint(1,7)
            if token == 7:
                self.boardArray[x[0]][x[1]] *= 2

    def removeLows(self):
        for x in range(self.dimension):
            for y in range(self.dimension):
                if self.boardArray[x][y] <= 4:
                    self.boardArray[x][y] = 0
            

    def removeValue(self, value: int) -> bool:
        empty = []
        for x in range(self.dimension):
            for y in range(self.dimension):
                if self.boardArray[x][y] == value:
                    empty.append((x,y))
        if len(empty) == 0:
            return False
        coord = random.choice(empty)
        self.boardArray[coord[0]][coord[1]] = 0 

    def checkOver(self, target: int) -> str:
        for x in self.boardArray:
            if target in x:
                return "win"

        for x in self.boardArray:
            if 0 in x:
                return "move"

        for x in range(self.dimension):
            for y in range(self.dimension):
                if self.possibleMoves(x, y) == True:
                    return "move"
        return "lost"

    def possibleMoves(self, x: int, y: int) -> bool:
        num = self.boardArray[x][y]
        if x-1 >= 0:
            if num == self.boardArray[x-1][y]:
                return True
        if x+1 < self.dimension:
            if num == self.boardArray[x+1][y]:
                return True
        if y-1 >= 0:
            if num == self.boardArray[x][y-1]:
                return True
        if y+1 < self.dimension:
            if num == self.boardArray[x][y+1]:
                return True
        return False

    def smash(self, move_in: str):
        if move_in == "down":
            for y in range(self.dimension):
                count = 0
                x = self.dimension - 1
                while x >= 0:
                    if self.boardArray[x][y] == 0:
                        for z in range(x, 0, -1):
                            self.boardArray[z][y] = self.boardArray[z-1][y]
                        self.boardArray[0][y] = 0
                        count += 1
                    else:
                        x -= 1
                    if count == self.dimension:
                        break

        if move_in == "up":
            for y in range(self.dimension):
                count = 0
                x = 0
                while x < self.dimension:
                    if self.boardArray[x][y] == 0:
                        for z in range(x, self.dimension - 1, 1):
                            self.boardArray[z][y] = self.boardArray[z+1][y]
                        self.boardArray[self.dimension - 1][y] = 0
                        count += 1
                    else:
                        x += 1
                    if count == self.dimension:
                        break
        if move_in == "right":
            for x in range(self.dimension):
                count = 0
                y = self.dimension - 1
                while y >= 0:
                    if self.boardArray[x][y] == 0:
                        for z in range(y, 0, -1):
                            self.boardArray[x][z] = self.boardArray[x][z-1]
                        self.boardArray[x][0] = 0
                        count += 1
                    else:
                        y -= 1
                    if count == self.dimension:
                        break

        if move_in == "left":
            for x in range(self.dimension):
                count = 0
                y = 0
                while y < self.dimension:
                    if self.boardArray[x][y] == 0:
                        for z in range(y, self.dimension - 1, 1):
                            self.boardArray[x][z] = self.boardArray[x][z+1]
                        self.boardArray[x][self.dimension - 1] = 0
                        count += 1
                    else:
                        y += 1
                    if count == self.dimension:
                        break

    def join(self, move_in: str):
        if move_in == "up" or move_in == "down":
            rowTarget, rowStart, increment = None, None, None
            if move_in == "down":
                rowTarget = 0
                rowStart = self.dimension - 1
                increment = -1
            else:
                rowTarget = self.dimension - 1
                rowStart = 0
                increment = 1
            for y in range(self.dimension):
                for x in range(rowStart, rowTarget, increment):
                    if self.boardArray[x][y] == self.boardArray[x + increment][y]:
                        self.boardArray[x][y] *= 2
                        for z in range(x + increment, rowTarget, increment):
                            self.boardArray[z][y] = self.boardArray[z + increment][y]
                        self.boardArray[rowTarget][y] = 0
        else:
            colTarget, colStart, increment = None, None, None
            if move_in == "right":
                colTarget = 0
                colStart = self.dimension - 1
                increment = -1
            else:
                colTarget = self.dimension - 1
                colStart = 0
                increment = 1
            for x in range(self.dimension):
                for y in range(colStart, colTarget, increment):
                    if self.boardArray[x][y] == self.boardArray[x][y + increment]:
                        self.boardArray[x][y] *= 2
                        for z in range(y + increment, colTarget, increment):
                            self.boardArray[x][z] = self.boardArray[x][z + increment]
                        self.boardArray[x][colTarget] = 0;

    def format(self, input: int) -> str:
        strInput = str(input)
        if len(strInput) == 1:
            return "  " + strInput + " "
        elif len(strInput) == 2:
            return " " + strInput + " "
        elif len(strInput) == 3:
            return " " + strInput
        elif len(strInput) == 4:
            return strInput
        else:
            return "    "

    def drawBoard(self):
        for x in self.boardArray:
            print("+----" * self.dimension + "+")
            for y in x:
                print ("|", end = "")
                tile = self.format(y)
                test = int(tile)
                if test == 2:
                    print(Fore.YELLOW + tile, end = "")
                    print(Style.RESET_ALL, end = "")
                elif test == 4:
                    print(Fore.BLUE + tile, end = "")
                    print(Style.RESET_ALL, end = "") 
                elif test == 8:
                    print(Fore.GREEN + tile, end = "")
                    print(Style.RESET_ALL, end = "")
                elif test == 16:
                    print(Fore.RED + tile, end = "")
                    print(Style.RESET_ALL, end = "")   
                elif test == 32:
                    print(Fore.MAGENTA + tile, end = "")
                    print(Style.RESET_ALL, end = "")
                elif test == 64:
                    print(Fore.CYAN + tile, end = "")
                    print(Style.RESET_ALL, end = "")
                elif test == 128:
                    print(Fore.BLUE + Back.YELLOW + tile, end = "")
                    print(Style.RESET_ALL, end = "")                             
                elif test == 256:
                    print(Fore.RED + Back.GREEN + tile, end = "")
                    print(Style.RESET_ALL, end = "") 
                elif test == 512:
                    print(Fore.CYAN + Back.RED + tile, end = "")
                    print(Style.RESET_ALL, end = "") 
                elif test == 1024:
                    print(Style.BRIGHT + Fore.RED + Back.WHITE + tile, end = "")
                    print(Style.RESET_ALL, end = "") 
                elif test == 2048:
                    print(Style.BRIGHT + Fore.CYAN + Back.WHITE + tile, end = "")
                    print(Style.RESET_ALL, end = "") 
                elif test == 4096:
                    print(Style.BRIGHT + Fore.MAGENTA + Back.WHITE + tile, end = "")
                    print(Style.RESET_ALL, end = "")
                elif test == 8192:
                    print(Style.BRIGHT + Fore.BLACK + Back.WHITE + tile, end = "")
                    print(Style.RESET_ALL, end = "")
                else:   
                    print("    ", end = "")
            print ("|")
        print("+----" * self.dimension + "+")





            


