#! /usr/bin/env python3
from copy import deepcopy
import subprocess
import random

""" Custom Errors """
class PositionInUse(Exception):
    pass

""" Stats Object """
class Stats:
    player1_score: int = 0
    player2_score: int = 0
    tie: int = 0

""" Main Game Class """
class MainGame:
    """ Initialize Self Variables """
    def __init__(self):
        self.emptyChar = "#"
        self.board  = [
            [self.emptyChar, self.emptyChar, self.emptyChar],
            [self.emptyChar, self.emptyChar, self.emptyChar],
            [self.emptyChar, self.emptyChar, self.emptyChar]
        ]
        self.players = (("Player1", "X"), ("Player2", "O"))
        self.startPlayer = random.choice(self.players)
        self.currentPlayer = None
        self.winningCombos = self.generateWinningCombos()
        self.errors = []
    
    """ Clears The Terminal """
    def clear(self):
        subprocess.call("cls||clear", shell=True)

    """ Print The Gameboard From self.board """
    def printBoard(self):
        self.clear()
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

    """ Checks If Given Mark Won """
    def isWinner(self, board: list, mark: str) -> bool:
        getBoard = lambda index: board[combo[index][0]][combo[index][1]]
        for combo in self.winningCombos:
            if (getBoard(0) == getBoard(1) == getBoard(2) == mark):
                return True
        return False

    """ Checks If The Board Is Full """
    def isBoardFull(self) -> bool:
        items = lambda index: self.board[index].count(self.emptyChar) == 0
        return True if items(0) and items(1) and items(2) else False

    """ Gets The Next Player From The Self.players List """
    def getNextPlayer(self) -> tuple:
        index = self.players.index(self.currentPlayer)
        return self.players[0] if index == len(self.players)-1 else self.players[index+1]
        
    """ Convert Input Coords Into List Indexes """
    def coordsToIndexex(self, coords: str) -> tuple:
        return (int(coords[1])-1, "ABC".find(coords[0]))

    """ Change Value Of Given Coords To The Currents Players Mark """
    def makeMove(self, indexes: tuple):
        if self.board[indexes[0]][indexes[1]] != self.emptyChar:
            raise PositionInUse
        self.board[indexes[0]][indexes[1]] = self.currentPlayer[1]

    """ Computer Move """
    def compMove(self):
        possibleMoves = []
        for rowIndex in range(len(self.board)):
            for itemIndex in range(len(self.board[rowIndex])):
                item = self.board[rowIndex][itemIndex]
                if item == self.emptyChar:
                    possibleMoves.append((rowIndex, itemIndex))

        # Firstly checks if it can win or block
        for player in self.players[::-1]: # reverse list so it checks if it can win first
           for move in possibleMoves:
               boardCopy = deepcopy(self.board)
               boardCopy[move[0]][move[1]] = player[1]
               
               if self.isWinner(boardCopy, player[1]):
                   return move

        # Take corners
        openCorners = []
        for move in possibleMoves:
            if move in ((0,0),(0,2),(2,0),(2,2)):
                openCorners.append(move)
        if len(openCorners) > 0:
            return random.choice(openCorners)

        # If middle is available
        if (1,1) in possibleMoves:
            return (1,1)

        openEdges = []
        for move in possibleMoves:
            if move in ((0,1),(1,0),(1,2),(2,1)):
                openEdges.append(move)
                
        if len(openEdges) > 0:
            return random.choice(openEdges)

    """ Get User Input """
    def getInput(self):
        return input(f"{self.currentPlayer[0]} ({self.currentPlayer[1]}) > ").upper()

    def addStats(self, action: str):
        if action == "win":
            if self.currentPlayer[0] == "Player1":
                Stats.player1_score += 1
            elif self.currentPlayer[0] == "Player2":
                Stats.player2_score += 1
        elif action == "tie":
            Stats.tie += 1
        
    """ Asks If User Wants To Play Again """
    def done(self, text: str):
        self.printBoard()
        print(text + "\n")

        playAgain= input("Do you want to play agan? (Y/n) > ")
        if playAgain == "n":
            return
        else:
            self.run()
        

    """ Main Gameloop """
    def gameloop(self):
        self.clear()
        print((
                "  _____ _        _____            _____          \n"
                " |_   _(_) ___  |_   _|_ _  ___  |_   _|__   ___ \n"
                "   | | | |/ __|   | |/ _` |/ __|   | |/ _ \ / _ \ \n"
                "   | | | | (__    | | (_| | (__    | | (_) |  __/\n"
                "   |_| |_|\___|   |_|\__,_|\___|   |_|\___/ \___|\n\n"
               f"    Player1 Score: {Stats.player1_score}   Tie: {Stats.tie}   Player2 Score: {Stats.player2_score} \n\n"
        ))

        print((
            "[0] Player vs Player\n"
            "[1] Player vs Computer\n"
            "[2] Exit"
        ))

        gamemode = input("Option > ")
        if gamemode == "2":
            return
        if gamemode not in ["0", "1"]:
            return print("Invalid option!")

        while 1:
            self.printBoard()
            self.errors.clear()
            self.currentPlayer = self.startPlayer if not self.currentPlayer else self.currentPlayer

            if gamemode == "0" or (gamemode == "1" and self.currentPlayer[1] == "X"):
                coords = self.getInput()

                if coords == "EXIT" or coords == "E":
                    return self.run()

                try:
                    indexes = self.coordsToIndexex(coords)
                    self.makeMove(indexes)
                except (IndexError, ValueError):
                    self.errors.append("Invalid coords!")
                    continue
                except PositionInUse: # Cleaner cause try block already used
                    self.errors.append("Position Is already in use")
                    continue

            if gamemode == "1" and self.currentPlayer[1] == "O":
                self.makeMove(self.compMove())

            # Check if win
            if self.isWinner(self.board, self.currentPlayer[1]):
                self.addStats("win")
                return self.done(f"{self.currentPlayer[0]} Won!")

            # Check if tie
            if self.isBoardFull():
                self.addStats("tie")
                return self.done("Tie!")

            self.currentPlayer = self.getNextPlayer()

    """ Main Run Function """
    def run(self):
        self.__init__()
        try: self.gameloop()
        except KeyboardInterrupt: print("\nQuitting!")
        
if __name__ == "__main__":
    MainGame().run()
