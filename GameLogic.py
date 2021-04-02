# AUTHOR: Garrett Born
# DATE: 08/13/2020
# DESCRIPTION: Oversees the board, logic, and moves for the board game BlackBox.

from Ray import *
import functools


def check_state(method):
    """Checks if game state is 'WON' or 'LOST'."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self._game_state == "PLAYING":
            result = method(self, *args, **kwargs)
            return result
        else:
            print("Not possible, since you already " + self._game_state + "!")
            return False

    return wrapper


class GameLogic:
    """Creates a BlackBox Game, which oversees a 10x10 board and game logic (score, guesses, atoms, etc.).
    Uses the Ray class to handle the logic of ray paths."""

    def __init__(self, atom_list):
        """Initializes BlackBox Game object with board, score, list of guesses made,
        list of ray entrances/exits, amount of atoms not guessed, and the game's state.
        Parameter: List of tuples with row, col location of atoms."""

        self._board = [
            [" ", u"\u2191", u"\u2191", u"\u2191", u"\u2191", u"\u2191", u"\u2191", u"\u2191", u"\u2191", " "],
            [u"\u2192", " ", " ", " ", " ", " ", " ", " ", " ", u"\u2190"],
            [u"\u2192", " ", " ", " ", " ", " ", " ", " ", " ", u"\u2190"],
            [u"\u2192", " ", " ", " ", " ", " ", " ", " ", " ", u"\u2190"],
            [u"\u2192", " ", " ", " ", " ", " ", " ", " ", " ", u"\u2190"],
            [u"\u2192", " ", " ", " ", " ", " ", " ", " ", " ", u"\u2190"],
            [u"\u2192", " ", " ", " ", " ", " ", " ", " ", " ", u"\u2190"],
            [u"\u2192", " ", " ", " ", " ", " ", " ", " ", " ", u"\u2190"],
            [u"\u2192", " ", " ", " ", " ", " ", " ", " ", " ", u"\u2190"],
            [" ", u"\u2193", u"\u2193", u"\u2193", u"\u2193", u"\u2193", u"\u2193", u"\u2193", u"\u2193", " "]]
        self._a_locations = atom_list
        self._score = 25
        self._guesses = []
        self._portals = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                         "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                         "U", "V", "W", "X", "Y", "Z"]
        self._atoms = len(atom_list)
        self._game_state = "PLAYING"

    def get_board(self):
        """Returns current board"""
        return self._board

    def print_board(self):
        """Prints board as grid with row and col numbering along edges."""

        board = self.get_board()
        row = 9
        while row > -1:
            print(row, board[row])
            row -= 1
        print("    0    1    2    3    4    5    6    7    8    9")

    def get_a_locations(self):
        """Returns list of tuples with atom locations"""
        return self._a_locations

    def get_score(self):
        """Returns current score"""
        return self._score

    def atoms_left(self):
        """Returns amount of atoms that haven't been guessed"""
        return self._atoms

    def get_guesses(self):
        """Returns list of row,col guesses already made"""
        return self._guesses

    def get_portals(self):
        """Returns list of row,col locations of entrances/exits of rays"""
        return self._portals

    def get_game_state(self):
        """Returns the current state of the game"""
        return self._game_state

    @check_state
    def shoot_ray(self, row, col):
        """Uses Ray object to conduct the shooting of a ray.
        Parameters: Row, col integers for location of ray entrance.
        Returns: False if game state is 'Win' or 'LOSE'
        or if row, col integers are not valid entrance locations;
        None if ray is blocked by atom; Tuple of row,col location of ray's exit"""
        # Uses validate method to check if row,col are legal for ray entrance location
        if not self.valid_ray(row, col):
            return False
        # creates ray object from row, col integers
        ray = Ray(row, col)
        # checks if atom is in front of entrance position
        if not ray.can_continue(self.get_a_locations()):
            self.mark_portal(ray.get_start())
            if self.get_score() <= 0:
                self.change_state("LOST")
            return None
        # while there is no atom in front of ray and ray will not exit board --
        while ray.can_continue(self.get_a_locations()):
            ray.check_diags(self.get_a_locations())
            # moves ray forward one space
            ray.advance()
        # if ray will exit board by advancing --
        if not ray.on_board():
            # adjusts score if entrance/exit do not match prior entrances/exits
            self.mark_portal(ray.get_start(), ray.get_pos())
            # changes state to lose if score is now <= 0
            if self.get_score() <= 0:
                self.change_state("LOST")
            # returns tuple of exit location
            return tuple(ray.get_pos())
        # if ray is blocked by atom --
        if not ray.no_atom(self.get_a_locations()):
            # changes state to lost if score is now <= 0
            self.mark_portal(ray.get_start())
            if self.get_score() <= 0:
                self.change_state("LOST")
            return None

    def mark_portal(self, start, pos=None):
        match_a = self._board[start[0]][start[1]]
        markers = self._portals
        if match_a == u"\u2190" or match_a == u"\u2191" or match_a == u"\u2192" or match_a == u"\u2193":
            self._board[start[0]][start[1]] = markers[0]
            self._score -= 1
        if pos is not None:
            match_b = self._board[pos[0]][pos[1]]
            if match_b == u"\u2190" or match_b == u"\u2191" or match_b == u"\u2192" or match_b == u"\u2193":
                self._board[pos[0]][pos[1]] = markers[0]
                self._score -= 1
        self._portals = self._portals[1:]
        return self._portals

    def valid_ray(self, row, col):
        """Validates if ray entrance location from shoot_ray is valid.
        Parameters: row, col integers for ray entrance from shoot_ray.
        Returns: True if row,col integers are valid; False if not valid."""
        # if row nor col is at an edge space, returns False
        if row != 0 and row != 9 and col != 0 and col != 9:
            return False
        # ensures no corner spaces have been selected
        if row == 0 or row == 9:
            if col > 8 or col < 1:
                return False
        if col == 0 or col == 9:
            if row > 8 or row < 1:
                return False
        return True

    @check_state
    def guess_atom(self, row, col):
        """Checks if guess matches the location of an atom and adjusts score and atom count accordingly.
        Parameters: row, col integers of player's guess.
        Returns: False if game state is 'WIN' or 'LOSE',
        or if row,col pair is in list of already made guesses,
        or if there is no atom at the guess location;
        True if guess location aligns with the location of an atom."""
        if not self.valid_guess(row, col):
            return False
        # if row,col in guess list, tells players and returns True
        if self._board[row][col] != " ":
            print("You've already guessed that location!")
            return True
        # if match found, deducts 1 from atoms list
        if (row, col) in self._a_locations:
            self._atoms -= 1
            # if all atoms guessed, changes game state to win and prints it
            if self._atoms == 0:
                self.change_state("WON")
                print(self.get_game_state())
            # adds guess location to list of guesses made and returns True
            self._board[row][col] = "A"
            return True
        # deducts 5 from score if no match and checks if you lost
        self._score -= 5
        if self._score <= 0:
            self.change_state("LOST")
            print(self.get_game_state())
        self._board[row][col] = "X"
        return False


    def valid_guess(self, row, col):
        """Validates if ray entrance location from shoot_ray is valid.
        Parameters: row, col integers for ray entrance from shoot_ray.
        Returns: True if row,col integers are valid; False if not valid."""
        # if row nor col is at an edge space, returns False
        if not isinstance(row, int) or not isinstance(col, int):
            return False
        # ensures no corner spaces have been selected
        if row < 1 or row > 8:
            return False
        if col < 1 or col > 8:
            return False
        return True


    def change_state(self, state):
        """Changes the game's current state.
        Parameter: String of new state.
        Returns: 'Invalid State' if new state is not in tuple of accepted game states;
        the game's new game state if the new state is valid."""
        # tuple of valid game states
        valid_state = ("WON", "LOST", "PLAYING")
        # if state received doesn't match above, tells player
        if state not in valid_state:
            return "Invalid State"
        # sets game state to new state
        self._game_state = state
        return self._game_state
