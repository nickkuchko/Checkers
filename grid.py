import turtle


class Grid(turtle.RawTurtle):              # defines a grid space and its properties

    gridSize = 60
    pawnRadius = 20
    crownRadius = 10

    def __init__(self, screen):
        self.screen = screen
        self.defaultAttributes()
        self.createPen()

    def createPen(self):
        super().__init__(self.screen)
        self.hideturtle()
        self.speed(0)
        self.width(0)
        self.up()

    def defaultAttributes(self):           # sets the grid's attributes
        self.gridX = 0
        self.gridY = 0
        self.colored = False               # True if the square is shaded, False if white
        self.selected = 0                  # 0 if space is normal, 1 or 2 if space is highlighted
        self.pawn = False                  # True if there is a pawn on the grid space
        self.player = 0                    # 1 if pawn is player1 (red), 2 if pawn is player2 (blue)
        self.king = False                  # True if pawn has been kinged

    def clearPawn(self):                   # removes the pawn from the grid
        self.selected = False
        self.pawn = False
        self.player = 0
        self.king = False
        self.draw()

    def importPawn(self, gridObj):         # imports all attributes from another grid object
        self.colored = gridObj.colored
        self.pawn = gridObj.pawn
        self.player = gridObj.player
        self.king = gridObj.king
        self.draw()

    def moveGrid(self, gX, gY):            # places the grid at a new set of coords
        self.gridX = gX
        self.gridY = gY

    def draw(self):                        # draws the grid
        pixleX = int(self.gridX * Grid.gridSize - 4 * Grid.gridSize)
        pixleY = int(self.gridY * Grid.gridSize - 4 * Grid.gridSize)
        self.clear()

        self.goto(pixleX, pixleY)
        self.seth(0)
        self.down()
        if(self.colored == True):
            if(self.selected in [1, 2]):
                self.color((0, 0, 0), (0.5, 1, 0.5))
            else:    
                self.color((0, 0, 0), (0.75, 0.75, 0.75))
            self.begin_fill()
        for f in range(4):
            self.fd(Grid.gridSize)
            self.left(90)
        self.end_fill()
        self.up()

        if(self.pawn == True):
            self.goto(pixleX + 0.5 * Grid.gridSize,pixleY + 0.5 * Grid.gridSize - Grid.pawnRadius)
            if(self.player == 1):
                self.color((0, 0, 0), (1, 0.5, 0.5))
            elif(self.player == 2):
                self.color((0, 0, 0), (0.5, 0.5, 1))
            else:
                self.color((0, 0, 0), (1, 0.5, 1))
            self.down()
            self.begin_fill()
            self.circle(Grid.pawnRadius, 360, 16)
            self.end_fill()
            self.up()

            if(self.king == True):
                self.goto(pixleX + 0.5 * Grid.gridSize,pixleY + 0.5 * Grid.gridSize - Grid.crownRadius)
                self.color((0, 0, 0),(1, 0.85, 0))
                self.down()
                self.begin_fill()
                self.circle(Grid.crownRadius, 360, 16)
                self.end_fill()
                self.up()
