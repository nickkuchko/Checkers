import turtle
import grid


class Titles(turtle.RawTurtle):                 # writes text on the screen

    def __init__(self, screen):
        self.screen = screen
        self.createPen()

    def createPen(self):
        super().__init__(self.screen)
        self.hideturtle()
        self.speed(0)
        self.width(0)
        self.up()

    def writeTurn(self, turn):
        if(turn == 1):
            string = "Red Player's Turn"
            self.color("red")
        elif(turn == 2):
            string = "Blue Player's Turn"
            self.color("blue")
        elif(turn == 0):
            string = "Turns are disabled"

        self.clear()
        self.goto(0, -5 * grid.Grid.gridSize)
        self.write(string, align="center", font=("Arial", 28, "normal"))
