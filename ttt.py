import random
import os, sys

""" Custom Errors """
class PositionInUse(Exception):
    pass

""" Main Game Class """
class MainGame:
    """ Initialize Self Variables """
    def __init__(self):
        self.board  = [
            ["#", "#", "#"],
            ["#", "#", "#"],
            ["#", "#", "#"]
        ]
        self.players = (("Player1", "X"), ("Player2", "O"))
        self.startPlayer = random.choice(self.players)
        self.currentPlayer = None
        self.winningCombos = self.generateWinningCombos()
        self.errors = []

    """ Print The Gameboard From self.board """
    def printBoard(self):
        os.system('cls||clear')
        
        print("\n  A  |  B  |  C  \n")
        print("     |     |")

        # Prints the board nicely
        for rowIndex in range(len(self.board)):
            print(''.join(
                    ''.join(f"  {self.board[rowIndex][itemIndex]}  " if itemIndex == 0 # Without "|" if first time
                            else f"|  {self.board[rowIndex][itemIndex]}  {''.join(f'  | {str(rowIndex + 1)}' if itemIndex == 2 else '')}")  # If not first time, print rowIndex only if last time
                                for itemIndex in range(len(self.board[rowIndex]))), # Loop
                    '_____|_____|_____\n     |     |', sep="\n" #Bottom
                )
        
        print(f"\n{self.errors[0]}\n" if self.errors != [] else "")

    " Generates A List Of Winning Combinations "
    def generateWinningCombos(self) -> list:
        combos = []
        for septype in range(3):
            if septype != 2:
                # Vertical and horizontal coordinates
                for line in range(3):
                    current = []
                    for item in range(3):
                        if septype == 0:
                            current.append((line, item))
                        elif septype == 1:
                            current.append((item, line))
                    combos.append(current)
            else:
                # Diagonal coordinates
                combos.append([(0,0), (1,1), (2,2)])
                combos.append([(0,2), (1,1), (2,0)])

        return combos

    """ Checks If The Current Player Won """
    def isWinner(self) -> bool:
        getBoard = lambda index: self.board[combo[index][0]][combo[index][1]]
        for combo in self.winningCombos:
            if (getBoard(0) == getBoard(1) == getBoard(2) == self.currentPlayer[1]):
                return True
        
        return False

    """ Gets The Next Player From The Self.players List """
    def getNextPlayer(self) -> tuple:
        index = self.players.index(self.currentPlayer)
        return self.players[0] if index == len(self.players)-1 else self.players[index+1]
        
    """ Convert Input Coords Into List Indexes """
    def coordsToIndexex(self, coords: str) -> tuple:
        return (int(coords[1])-1, "ABC".find(coords[0]))

    """ Change Value Of Given Coords To The Currents Players Mark """
    def makeMove(self, coords: str):
        indexes = self.coordsToIndexex(coords)
        if self.board[indexes[0]][indexes[1]] != "#":
            raise PositionInUse
        self.board[indexes[0]][indexes[1]] = self.currentPlayer[1]

    """ Asks If User Wants To Play Again """
    def done(self, text: str):
        self.printBoard()
        print(text + "\n")

        playAgain= input("Do you want to play agan? (Y/n) > ")
        if playAgain == "n":
            sys.exit(0)
        else:
            self.run()
        

    """ Main Gameloop """
    def gameloop(self):
        while 1:
            self.printBoard()
            self.errors.clear()
            self.currentPlayer = self.startPlayer if not self.currentPlayer else self.currentPlayer
            coords = input(f"{self.currentPlayer[0]} ({self.currentPlayer[1]}) > ").upper()

            if coords == "EXIT" or coords == "E":
                return print("Quitting!")

            try: 
                self.makeMove(coords)
            except (IndexError, ValueError):
                self.errors.append("Invalid coords!")
                continue
            except PositionInUse:
                self.errors.append("Position Is already in use")
                continue
            
            
            # Check if win
            if self.isWinner():
                return self.done(f"{self.currentPlayer[0]} Won!")

            # Check if tie ( put here so it doesen't have to run even if won )
            else:
                items = ""
                for line in self.board:
                    for item in line:
                        items += item 

                if not "#" in items:
                    return self.done("Tie")

            self.currentPlayer = self.getNextPlayer()

    """ Main Run Function """
    def run(self):
        self.__init__()
        try: self.gameloop()
        except KeyboardInterrupt: print("\nQuitting!")
        
if __name__ == "__main__":
    MainGame().run()
