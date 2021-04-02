instructions = ["BlackBox is a board game created in the 1970s. It can be played by one or two players.",
                " ",
                "The objective of the game is to find atoms hidden within the grid. The guessing player",
                "shoots rays from spaces containing arrows. The ray follows the path of the arrow",
                "starting from the entrance. If its path crosses  an atom, it will hit it and not exit",
                "the board. If the ray's path is not obstructed, it will exit the board from the ",
                "corresponding marked border space. If the ray encounters an atom to its diagonal, it",
                "will be deflected at a 90 degree angle in the direction opposite the atom. For example,",
                "if an atom is located to the ray's left diagonal, the ray will be deflected to the right,",
                "away from the atom. Based on the entrances and exits of each ray, the guessing player",
                "can then guess the coordinates of each atom (up to 5 allowed on the board).",
                " ",
                "The guessing player starts with a score of 25. For each border space a ray enters/exits,",
                "1 point is deducted from the score. For each incorrect guess, 5 points are deducted.",
                "The game is won when the guessing player has guessed all of the atoms on the board.",
                "The game is lost when the guessing player's score drops to or below 0."]

with open("instructions.txt", "w") as outfile:
    for i in range(len(instructions)):
        outfile.write(instructions[i] + "\n")
