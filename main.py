from GameLogic import *
from Board import *
import random


def display_title():
    title = ["  ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗  ██████╗ ██╗  ██╗",
             "  ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗╚██╗██╔╝",
             "  ██████╔╝██║     ███████║██║     █████╔╝ ██████╔╝██║   ██║ ╚███╔╝",
             "  ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██║   ██║ ██╔██╗",
             "  ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██████╔╝╚██████╔╝██╔╝ ██╗",
             "  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝",
             "                                                    by GARRETT BORN"]
    for line in range(len(title)):
        print(title[line])
    print()


def create_board(game_board):
    current = Board(game_board)
    current.top_row()
    current.middle_rows()
    current.last_row()


def instructions():
    print("INSTRUCTIONS " + u"\u2550" * 57)
    print()
    with open('instructions.txt', 'r') as infile:
        for line in infile:
            print(line.strip())
    print()
    print(u"\u2550" * 70)
    print()


def setup(players):
    try:
        val = int(players)
        if val > 2 or val < 1:
            retry = input("Sorry, only 1 or 2 players are allowed. Try again: ")
            return setup(retry)
        elif val == 2:
            atoms = input("How many atoms would you like to place (Between 1 and 5)? ")
            return atoms_for_two(atoms)
        else:
            print("Time for random!")
            return atoms_for_one(random.randint(1, 5))
    except ValueError:
        try_again = input("Sorry, only 1 or 2 players are allowed. Try again: ")
        return setup(try_again)


def atoms_for_two(count):
    try:
        val = int(count)
        if val > 5 or val < 1:
            retry = input("Sorry, you can only place between 1 and 5 atoms. Try again: ")
            return atoms_for_two(retry)
        atoms = []
        while val > 0:
            row = input("Select a row (y-coord) to place your atom on (between 1 and 8): ")
            y = atom_coord(row)
            col = input("Select a column (x-coord) to place your atom on (between 1 and 8): ")
            x = atom_coord(col)
            atom = (y, x)
            if atom not in atoms:
                atoms.append(atom)
                val -= 1
            else:
                print("Sorry, you've already placed an atom at (" + str(row) + ", " + str(col) + ").")
        print("Great! You've placed " + str(count) + " atoms. Let's play!")
        print()
        return atoms
    except ValueError:
        try_again = input("Sorry, you can only place between 1 and 5 atoms. Try again: ")
        return atoms_for_two(try_again)


def atom_coord(coord, type=0):
    try:
        val = int(coord)
        if val > 8 or val < 1:
            if type == 0:
                retry = input("Sorry, atom must be placed between spaces 1 and 8. Try again: ")
                return atom_coord(retry)
            else:
                retry = input("Sorry, guess must be between spaces 1 and 8. Try again: ")
                return atom_coord(retry, 1)
        return coord
    except ValueError:
        if type == 0:
            retry = input("Sorry, atom must be placed between spaces 1 and 8. Try again: ")
            return atom_coord(retry)
        else:
            retry = input("Sorry, guess must be between spaces 1 and 8. Try again: ")
            return atom_coord(retry, 1)


def atoms_for_one(amount):
    atoms = []
    while amount > 0:
        row = random.randint(1, 8)
        col = random.randint(1, 8)
        atom = (row, col)
        while atom in atoms:
            row = random.randint(1, 8)
            col = random.randint(1, 8)
            atom = (row, col)
        atoms.append(atom)
        amount -= 1
    print("Great! You have", len(atoms), "atoms to find. Good luck!")
    return atoms


display_title()
question = input("Played before?" + "\n" + "Enter 'i' for instructions or any other key to continue: ")
print()
if question.lower() == "i":
    instructions()
game_type = input("Enter '1' to play a 1-player game or '2' for a 2-player game: ")
game = GameLogic(setup(game_type))
print()
create_board(game.get_board())
while game.get_game_state() == "PLAYING":
    response = input("Would you like to shoot a ray or guess an atom?" + "\n"
                     + "Enter 's' to shoot a ray or 'g' to guess an atom: ")
    while response != "g" and response != "s":
        response = input("Sorry, please enter 's' to shoot a ray or 'g' to guess an atom: ")
    if response == "s":
        row = input("Please choose which row you would like to shoot a ray from." + "\n"
                    + "Remember, the ray can only be shot through a border space: ")

        col = input("Please choose which column you would like to shoot a ray from." + "\n"
                    + "Remember, the ray can only be shot through a border space: ")
        ray = game.shoot_ray(int(row), int(col))
        while ray is False:
            row = input("Sorry, that ray location wasn't valid." + "\n"
                      + "Please choose a valid row to shoot your ray from: ")
            cow = input("Please choose a valid column to shoot your ray from." + "\n"
                      + "Remember, the ray can only be shot through a border space: ")
            ray = game.shoot_ray(int(row), int(col))
    elif response == "g":
        r = atom_coord(input("Select the row (y-coord) you believe an atom to be located on (between 1 and 8): "), 1)
        c = atom_coord(input("Select the column (x-coord) you believe an atom to be located on (between 1 and 8): "), 1)
        print(game.get_a_locations())
        game.guess_atom(int(r), int(c))
    print()
    print("Current score: ", game.get_score())
    print("Atoms remaining: ", game.atoms_left())
    print()
    create_board(game.get_board())
if game.get_game_state() == "WON":
    print("Congrats! You " + game.get_game_state())
else:
    print("Sorry! You " + game.get_game_state())
