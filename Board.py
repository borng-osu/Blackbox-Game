class Board:

    def __init__(self, board):
        self._info = board

    def top_row(self):
        """Constructs and prints top row of Blackbox game board to be viewable on console."""
        info = self._info
        portals = ""
        for p in range(1, 9):
            portals += u"\u2502" + " " * 2 + info[9][p] + " " * 2
        print("9 " + " " * 2 + portals + u"\u2502" + " " * 2)
        print("  " + u"\u2500" * 2 + (u"\u253C" + u"\u2500" * 5) * 8 + u"\u253C" + u"\u2500" * 2)

    def middle_rows(self):
        """Constructs and prints middle rows of Blackbox game board to be viewable on console."""
        info = self._info
        spaces = ""
        for row in range(8, 0, -1):
            spaces += str(row) + " " + info[row][0] + " "
            for col in range(1, 9):
                spaces += u"\u2502" + " " * 2 + info[row][col] + " " * 2
            spaces += u"\u2502" + " " + info[row][9]
            print(spaces)
            print("  " + u"\u2500" * 2 + (u"\u253C" + u"\u2500" * 5) * 8 + u"\u253C" + u"\u2500" * 2)
            spaces = ""
        #print(u"\u263C" + " " + (u"\u2502" + " " * 5) * 8 + u"\u2502" + " " + u"\u263C")
        #print(u"\u2500" * 2 + (u"\u253C" + u"\u2500" * 5) * 8 + u"\u253C" + u"\u2500" * 2)

    def last_row(self):
        """Constructs and prints last row of Blackbox game board to be viewable on console."""
        info = self._info
        portals = ""
        for p in range(1, 9):
            portals += u"\u2502" + " " * 2 + info[0][p] + " " * 2
        print("0 " + " " * 2 + portals + u"\u2502" + " " * 2)
        print(" 0     1     2     3     4     5     6     7     8     9")
