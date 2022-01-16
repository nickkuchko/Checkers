import grid
import titles
import turtle
from datetime import datetime
from random import randint


gameTitle = "Easy Checkers"
w = turtle.Screen()
w.tracer(0, 0)
w.title(gameTitle)

def onGrid(x, y):                              # checks if coordinates are on the board
    return 0 <= x < 8 and 0 <= y < 8

def logToConsole(*strings):                    # prints a log string 
    dt = datetime.today()
    print("<%02i/%02i/%04i" % (dt.day,dt.month,dt.year), end=" ")
    print("%02i:%02i:%02i>" % (dt.hour,dt.minute,dt.second), end=" ")
    for string in strings:
        print(string, end="")
    print()


class Checkers:

    def __init__(self, screen):
        self.screen = screen
        self.resetGame()
        self.createTitles()

    def resetGame(self):                   
        self.turn = randint(1, 2)
        self.createGrid()

    def createGrid(self):
        self.matrix = [[None]*8 for _ in range(8)]

        for x in range(8):                     # fill the matrix with grid objects and assign them attributes
            for y in range(8):
                self.matrix[x][y] = grid.Grid(self.screen)
                self.matrix[x][y].moveGrid(x,y)
                if(((x + y) % 2) == 1):
                    self.matrix[x][y].colored = True
                    if(y in [0, 1, 2]):
                        self.matrix[x][y].pawn = True
                        self.matrix[x][y].player = 1
                    if(y in [5, 6, 7]):
                        self.matrix[x][y].pawn = True
                        self.matrix[x][y].player = 2
                self.matrix[x][y].draw()

        self.highlightedSpaces = []            # create list to hold values of highlighted spaces
        self.spaceSelected = False

    def createTitles(self):
        self.text0 = titles.Titles(self.screen)
        self.text1 = titles.Titles(self.screen)
        self.text1.writeTurn(self.turn)

    def mouseEvent(self, pixelX, pixelY):         # is called whenever the window is clicked
        x = int((pixelX + 4 * grid.Grid.gridSize) // grid.Grid.gridSize)
        y = int((pixelY + 4 * grid.Grid.gridSize) // grid.Grid.gridSize)
        if(onGrid(x,y) == True):
            logToConsole("\tMouse event at coords (%s,%s)" % (x,y))

            if((self.matrix[x][y].pawn == True) and (self.matrix[x][y].player == self.turn)):                  # if grid clicked contains a pawn and the current player it, highlight it's possible moves
                if(self.spaceSelected != 0):
                    self.deselectAll()
                moves = self.findMoves(x, y)
                jumps = self.findJumps(x, y)
                for move in moves:
                    self.matrix[move[0]][move[1]].selected = 1
                    self.highlightedSpaces.append((move[0],move[1]))
                    self.matrix[move[0]][move[1]].draw()
                for move in jumps:
                    self.matrix[move[0]][move[1]].selected = 2
                    self.highlightedSpaces.append((move[0],move[1]))
                    self.matrix[move[0]][move[1]].draw()
                self.spaceSelected = (x, y)
                logToConsole("\tMoves highlighted for pawn at (%s,%s)" % (x, y))

            elif(self.matrix[x][y].selected == 1):                     # move the selected pawn (if grid clicked can be moved )
                self.movePawn(self.spaceSelected,(x, y))
                self.deselectAll()
                self.endTurn()

            elif(self.matrix[x][y].selected == 2):                     # jump the selected pawn (if grid clicked can be jumped)
                self.jumpPawn(self.spaceSelected,(x, y))
                jumps = self.findJumps(x, y)
                if(jumps != []):
                    self.deselectAll()
                    self.spaceSelected = (x, y)
                    for move in jumps:
                        self.matrix[move[0]][move[1]].selected = 2
                        self.highlightedSpaces.append((move[0],move[1]))
                        self.matrix[move[0]][move[1]].draw()
                else:
                    self.deselectAll()
                    self.endTurn()
            else:
                self.deselectAll()
            logToConsole("\tMouse event completed\n")

    def deselectAll(self):
        for space in self.highlightedSpaces:
            self.matrix[space[0]][space[1]].selected = 0
            self.matrix[space[0]][space[1]].draw()
        self.spaceSelected = False
        logToConsole("\tAll spaces un-highlited")

    def findMoves(self, x, y):                         # returns moves available to a pawn 
        if(self.matrix[x][y].player == 1):
            moves = [(-1, 1), (1, 1)]
            if(self.matrix[x][y].king == 1):
                moves += [(-1, -1), (1, -1)]

        elif(self.matrix[x][y].player == 2):
            moves = [(-1, -1), (1, -1)]
            if(self.matrix[x][y].king == 1):
                moves += [(-1, 1), (1, 1)]

        coords = []
        for move in moves:
            x1 = x + move[0]
            y1 = y + move[1]
            if((onGrid(x1, y1) == True) and (self.matrix[x1][y1].pawn == False)):
                coords.append((x1, y1))
        return coords

    def findJumps(self, x, y):                         # returns coords of jumps available to a pawn
        if(self.matrix[x][y].player == 1):
            moves = [(-1, 1), (1, 1)]
            if(self.matrix[x][y].king == 1):
                moves += [(-1, -1), (1, -1)]

        elif(self.matrix[x][y].player == 2):
            moves = [(-1, -1), (1, -1)]
            if(self.matrix[x][y].king == 1):
                moves += [(-1, 1), (1, 1)]

        coords = []
        for move in moves:
            x1 = x + move[0]
            y1 = y + move[1]
            x2 = x + 2*move[0]
            y2 = y + 2*move[1]
            if((onGrid(x2, y2) == True) and (self.matrix[x2][y2].pawn == False)):
                if((self.matrix[x1][y1].pawn == True)):
                    if((self.matrix[x][y].player == 1) and (self.matrix[x1][y1].player == 2)):
                        coords.append((x2, y2))
                    elif((self.matrix[x][y].player == 2) and (self.matrix[x1][y1].player == 1)):
                        coords.append((x2, y2))
        return coords

    def movePawn(self, gridA, gridB):
        self.matrix[gridB[0]][gridB[1]].importPawn(self.matrix[gridA[0]][gridA[1]])
        self.matrix[gridA[0]][gridA[1]].clearPawn()
        self.kingPawn(gridB[0],gridB[1])
        logToConsole("\tMoved pawn at %s to %s" % (gridA, gridB))

    def jumpPawn(self, gridA, gridC):                  # moves a pawn from gridA to gridC by jumping over the pawn in gridB
        gridB = (int((gridC[0]+gridA[0])/2),int((gridC[1]+gridA[1])/2))
        self.matrix[gridC[0]][gridC[1]].importPawn(self.matrix[gridA[0]][gridA[1]])
        self.matrix[gridB[0]][gridB[1]].clearPawn()
        self.matrix[gridA[0]][gridA[1]].clearPawn()
        self.kingPawn(gridC[0],gridC[1])
        logToConsole("\tPawn at %s jumped over pawn at %s to coords %s" % (gridA, gridB, gridC))

    def kingPawn(self, x, y):                          # kings the pawn at coords (if it has reached the kings row)
        if((self.matrix[x][y].player == 1) and (y == 7)):
            self.matrix[x][y].king = True
            self.matrix[x][y].draw()
            logToConsole("\tPawn at (%s,%s) was kinged" % (x,y))
        elif((self.matrix[x][y].player == 2) and (y == 0)):
            self.matrix[x][y].king = True
            self.matrix[x][y].draw()
            logToConsole("\tPawn at (%s,%s) was kinged" % (x,y))

    def endTurn(self):
        if(self.turn == 1):
            logToConsole("\tRed Player's turn has ended")
            self.turn = 2
        elif(self.turn == 2):
            logToConsole("\tBlue Player's turn has ended")
            self.turn = 1
        self.text1.writeTurn(self.turn)


if __name__ == "__main__":
   
    logToConsole("\tRunning game: ", gameTitle)
    game = Checkers(w)

    w.onclick(game.mouseEvent)
    logToConsole("\tMouse event attatched to window")
    logToConsole("\tBeginning main program loop...\n")
    w.mainloop()

    logToConsole("\tMain program loop ended")
