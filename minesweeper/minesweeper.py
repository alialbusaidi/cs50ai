import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # We know that every cell in self.cells is a mine when the number of cells is equal to the count of mines?
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base 
        #    based on the value of `cell` and `count`
        # Find surrounding cells
        neighors = set()
        # Loop over all cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # If current iteration is at
                if (i, j) == cell:
                    continue
                
                # iteration is within bound of board
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighors.add((i, j))

        known = neighors & self.mines
        unknown = neighors - self.safes - self.mines

        updated_count = count - len(known)

        # Create new sentence with surrounding cells and count as input
        s0 = Sentence(unknown, updated_count)
    
        # Add new sentence to knowledge
        self.knowledge.append(s0)

        while True:
            delta = False

            new_safes = set()
            new_mines = set()

            for sentence in self.knowledge:
                new_safes |= sentence.known_safes()
                new_mines |= sentence.known_mines()

            if new_safes or new_mines: 
                delta = True

            for c in new_safes:
                self.mark_safe(c)
            for c in new_mines:
                self.mark_mine(c)
            
            # 4) mark any additional cells as safe or as mines
            #    if it can be concluded based on the AI's knowledge base   
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 is s2: 
                        continue
                    elif s2.cells.issubset(s1.cells):
                        s3_cells = s1.cells - s2.cells
                        s3_count = s1.count - s2.count
                        s3 = Sentence(s3_cells, s3_count)
                        if s3_cells and s3 not in self.knowledge:
                            self.knowledge.append(s3)
                            delta = True     
                    elif s1.cells.issubset(s2.cells):
                        s3_cells = s2.cells - s1.cells
                        s3_count = s2.count - s1.count
                        s3 = Sentence(s3_cells, s3_count)
                        if s3_cells and s3 not in self.knowledge:
                            self.knowledge.append(s3)
                            delta = True
                    else: 
                        continue

            self.knowledge = [s for s in self.knowledge if s.cells]

            if not delta: 
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        availble_moves = list(self.safes - self.moves_made)
        if not availble_moves: 
            return None
        else: 
            return random.choice(availble_moves)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                all_moves.add((i, j))

        legal_moves = list(all_moves - self.moves_made - self.mines)

        if not legal_moves: 
            return None
        else: 
            return random.choice(legal_moves)
            