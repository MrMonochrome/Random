from colorama import Fore

class GameBoard(object):
    def __init__(self):
        self.board = [[0 for x in range(8)] for y in range(8)]
        self.score = [2, 2]
        self.playerColours = [Fore.BLUE, Fore.RED]
        self.playerCharacters = [".", self.playerColours[0] + "©" + Fore.RESET,
                                 self.playerColours[1] + "ø" + Fore.RESET]
        for x in range(3, 5):
            self.board[x][x] = 1
            self.board[7 - x][x] = 2

    def getRowTerminator(self, x):
        if x == 7:
            return "\n"
        return " "

    def drawBoard(self, showFlipCountForPlayerNumber):
        for y in reversed(range(0, 8)):
            print(y, end=' ')
            for x in range(0, 8):
                piece = self.board[x][y]

                print(self.getBoardCharacter(x, y, showFlipCountForPlayerNumber), end=self.getRowTerminator(x))
        print('  ', end='')
        for x in range(0, 8):
            print(x, end=self.getRowTerminator(x))

    def getBoardCharacter(self, x, y, showFlipCountForPlayerNumber):
        piece = self.board[x][y]

        if piece > 0 or showFlipCountForPlayerNumber == 0:
            return self.playerCharacters[piece]

        flipCount = self.assessMove(showFlipCountForPlayerNumber, x, y, overturnPieces=False)
        if flipCount == 0:
            return "."

        return self.getPlayerColour(showFlipCountForPlayerNumber) + "." + Fore.RESET

    def getPlayerCharacter(self, playerNumber):
        return self.playerCharacters[playerNumber]

    def getPlayerColour(self, playerNumber):
        return self.playerColours[playerNumber - 1]

    def positionIsEmpty(self, x, y):
        return self.board[x][y] == 0

    def getPlayerAtPosition(self, x, y):
        return self.board[x][y]

    def tryToMakeMove(self, playerNumber, x, y):
        if not self.positionIsEmpty(x, y):
            return False

        totalFlipCount = self.assessMove(playerNumber, x, y, overturnPieces=True)
        if totalFlipCount > 0:
            self.board[x][y] = playerNumber
            self.score[playerNumber - 1] += totalFlipCount + 1
            self.score[self.opponentNumber(playerNumber) - 1] -= totalFlipCount

        return totalFlipCount

    def assessMove(self, playerNumber, x, y, overturnPieces):
        totalFlipCount = 0

        for stepX in range(-1, 2):
            for stepY in range(-1, 2):
                if not (stepY == 0 and stepX == 0):
                    flipCount = self.getFlipCount(playerNumber, x, y, stepX, stepY)
                    totalFlipCount += flipCount
                    if overturnPieces and flipCount > 0:
                        self.overturnRow(playerNumber, x, y, stepX, stepY)

        return totalFlipCount

    def opponentNumber(self, playerNumber):
        return 3 - playerNumber

    def getFlipCount(self, playerNumber, startFromX, startFromY, stepX, stepY):
        opponent = self.opponentNumber(playerNumber)
        x = startFromX
        y = startFromY
        flipCount = 0
        while True:
            x += stepX
            y += stepY
            if self.isPassedEdge(x) or self.isPassedEdge(y):
                flipCount = 0
                break

            piece = self.board[x][y]
            if piece == opponent:
                flipCount += 1
                continue
            elif piece == 0:
                flipCount = 0
            break

        return flipCount

    def overturnRow(self, playerNumber, x, y, stepX, stepY):
        opponent = self.opponentNumber(playerNumber)
        while True:
            x += stepX
            y += stepY
            if self.isPassedEdge(x) or self.isPassedEdge(y):
                break

            piece = self.board[x][y]
            if piece == opponent:
                self.board[x][y] = playerNumber
            else:
                break

    def isPassedEdge(self, coordinate):
        return coordinate < 0 or coordinate > 7

    def gameIsDrawn(self):
        return self.score[0] == 32 and self.score[1] == 32

    def playerHasWon(self, playerNumber):
        opponent = self.opponentNumber(playerNumber)
        if self.score[opponent - 1] == 0: #Opponent wiped out
            return True

        if sum(self.score) == 64\
                and self.score[opponent - 1] < self.score[playerNumber - 1]: #Board filled
            return True

        return False

    def showScore(self):
        print("Score: {0} = {1}, {2} = {3}".format(self.getPlayerCharacter(1), self.score[0],
                                                   self.getPlayerCharacter(2), self.score[1]))

