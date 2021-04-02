
class Ray:
    """Creates a Ray, which oversees teh logic of a ray created by a BlackBox Game's shoot_ray method.
    Logic includes ray's direction, turning if an atom is in its diagonal,
    checking if it can continue, and advancing."""

    def __init__(self, start_row, start_col):
        """Initializes ray object with start location, position, and direction.
        Parameters: Integers for row and col start."""
        self._start = (start_row, start_col)
        self._pos = [start_row, start_col]
        self._direction = self.set_direction(start_row, start_col)

    def set_direction(self, row, col):
        """Initializes ray's direction.
        Parameters: Integers for row and col start."""
        if row == 9:
            return "N"
        if row == 0:
            return "S"
        if col == 0:
            return "E"
        if col == 9:
            return "W"

    def get_direction(self):
        """Returns ray's current direction"""
        return self._direction

    def get_pos(self):
        """Returns ray's current position"""
        return self._pos

    def get_start(self):
        """Returns ray's starting location"""
        return self._start

    def advance(self):
        """Advances ray one space forward based on position and direction."""
        position = self._pos
        if self._direction == "N":
            current = position[0]
            position[0] = current - 1
            self._pos = position
            return self._pos
        if self._direction == "S":
            current = position[0]
            position[0] = current + 1
            self._pos = position
            return self._pos
        if self._direction == "E":
            current = position[1]
            position[1] = current + 1
            self._pos = position
            return self._pos
        if self._direction == "W":
            current = position[1]
            position[1] = current - 1
            self._pos = position
            return self._pos

    def can_continue(self, atom_list):
        if self.on_board():
            return self.no_atom(atom_list)
        return False

    def no_atom(self, atom_list):
        """Checks if ray can continue and if an atom is in front of the ray.
        Parameter: List of atom locations, a list of tuples."""
        pos = tuple(self._pos)
        for atom in range(len(atom_list)):
            if pos == atom_list[atom]:
                return False
        return True

    def on_board(self):
        """Checks if the ray will exit the board if it advances."""
        pos = self._pos
        if self.get_direction() == "N":
            if pos[0] - 1 < 0:
                return False
            return True
        if self.get_direction() == "S":
            if pos[0] + 1 > 9:
                return False
            return True
        if self.get_direction() == "E":
            if pos[1] + 1 > 9:
                return False
            return True
        if self.get_direction() == "W":
            if pos[1] - 1 < 0:
                return False
            return True

    def check_diags(self, atom_list):
        # checks diagonals for atoms
        l_diag = self.check_l_diag(atom_list)
        r_diag = self.check_r_diag(atom_list)
        # changes direction via ray's turn methods if atom is found
        if l_diag == 1:
            if r_diag == 1:
                self.u_turn()
            self.r_turn()
        if r_diag == 1:
            self.l_turn()
        return

    def check_l_diag(self, atom_list):
        """Checks if atom is located at the left, forward diagonal of the ray's current position.
        Parameter: BlackBox Game board, a list of 10 lists."""
        pos = self.get_pos()
        if self.get_direction() == "N":
            if pos[1] - 1 < 0:
                return 0
            left = (pos[0] - 1, pos[1] - 1)
            if left in atom_list:
                return 1
        if self.get_direction() == "S":
            if pos[1] + 1 > 9:
                return 0
            left = (pos[0] + 1, pos[1] + 1)
            if left in atom_list:
                return 1
        if self.get_direction() == "E":
            if pos[0] + 1 > 9:
                return 0
            left = (pos[0] - 1, pos[1] + 1)
            if left in atom_list:
                return 1
        if self.get_direction() == "W":
            if pos[0] - 1 < 0:
                return 0
            left = (pos[0] + 1, pos[1] - 1)
            if left in atom_list:
                return 1
        return 0

    def check_r_diag(self, atom_list):
        """Checks if atom is located at the left, forward diagonal of the ray's current position.
        Parameter: BlackBox Game board, a list of 10 lists."""
        pos = self.get_pos()
        if self.get_direction() == "N":
            if pos[1] + 1 > 9:
                return 0
            right = (pos[0] - 1, pos[1] + 1)
            if right in atom_list:
                return 1
        if self.get_direction() == "S":
            if pos[1] - 1 < 0:
                return 0
            right = (pos[0] + 1, pos[1] - 1)
            if right in atom_list:
                return 1
        if self.get_direction() == "E":
            if pos[0] + 1 > 9:
                return 0
            right = (pos[0] + 1, pos[1] + 1)
            if right in atom_list:
                return 1
        if self.get_direction() == "W":
            if pos[0] - 1 < 0:
                return 0
            right = (pos[0] - 1, pos[1] - 1)
            if right in atom_list:
                return 1
        return 0

    def r_turn(self):
        """Turns the ray's direction to the right based on its current direction."""
        if self.get_direction() == "N":
            self._direction = "E"
            return self._direction
        if self.get_direction() == "S":
            self._direction = "W"
            return self._direction
        if self.get_direction() == "E":
            self._direction = "S"
            return self._direction
        if self.get_direction() == "W":
            self._direction = "N"
            return self._direction

    def l_turn(self):
        """Turns the ray's direction to the left based on its current direction."""
        if self.get_direction() == "N":
            self._direction = "W"
            return self._direction
        if self.get_direction() == "S":
            self._direction = "E"
            return self._direction
        if self.get_direction() == "E":
            self._direction = "N"
            return self._direction
        if self.get_direction() == "W":
            self._direction = "S"
            return self._direction

    def u_turn(self):
        """Reverses ray's direction based on its current direction."""
        if self.get_direction() == "N":
            self._direction = "S"
            return self._direction
        if self.get_direction() == "S":
            self._direction = "N"
            return self._direction
        if self.get_direction() == "E":
            self._direction = "W"
            return self._direction
        if self.get_direction() == "W":
            self._direction = "E"
            return self._direction