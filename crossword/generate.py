import sys

from crossword import Crossword, Variable
from crossword import *




class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # For each variable in the crossword
        for variable in self.crossword.variables:
            # For each word in that variable's domain
            for word in list(self.domains[variable]):
                # If that word doesn't meet the unary constraint, i.e. if length of word isn;t same as length of variable
                if len(word) != variable.length:
                    # Remove that word from the domain of the variable
                    self.domains[variable].remove(word)

    

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Initialize revised variable to False
        revised = False

        # Save overlap indices (if any) in variable
        overlaps = self.crossword.overlaps[x, y]

        # If overlap exists between variables, continue to loop over x's domain
        if overlaps:
            # For each value in x variable domain
            for x_word in list(self.domains[x]):
                # Check against all value in y variable domain
                if not any(x_word[overlaps[0]] == y_word[overlaps[1]] for y_word in list(self.domains[y])):
                    self.domains[x].remove(x_word)
                    revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # If arcs list is None, consider all arcs in problem
        if arcs is None:
            arcs = self.all_arcs()

        # While arcs is not empty
        while len(arcs) != 0:
            # Dequeue a pair of variables (Arc) to enforce consistency
            x, y = arcs.pop()
            
            # If any revision is done after enforcing arc consistency, 
            if self.revise(x, y):
                # Check if domain of x is empty, then unsolvable
                if len(self.domains[x]) == 0:
                    return False
                # For all neighbors of x, add to queue to check for consistency
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))
        return True

        
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check to see if all variables are in the assignment dict
        if len(self.crossword.variables) == len(assignment):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check that all values (words) are distinct
        # Create set of assignment dict values, then compare length of set to assignment length
        distinct_values = set(assignment.values())

        if len(distinct_values) != len(assignment):
            return False

        # For each variable, check:
        for var in assignment:
            # Each Value (word) is the correct length
            if len(assignment[var]) != var.length:
                return False
            # There are no conflict between neighboring variables
            for neighbor in self.crossword.neighbors(var):
                # Skip if the neighbor is not assigned
                if neighbor not in assignment:
                    continue

                overlaps = self.crossword.overlaps[var, neighbor]
                if assignment[var][overlaps[0]] != assignment[neighbor][overlaps[1]]:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        var_domain = list(self.domains[var])
        # Create domain dict
        var_domain_n = dict()
        # Get a list of that variables neighbors
        neighbors = list(self.crossword.neighbors(var))

        # For each word in the domain of var
        for word in var_domain:
            eliminated_words = 0
            for neighbor in neighbors:
                neighbors_domain = self.domains[neighbor]
                # Get overlaps between current variable and current neighbor 
                i, j = self.crossword.overlaps[var, neighbor]
                # For each word elimination in the neighbors domain, increase a count
                for neighbor_word in neighbors_domain:
                    if word[i] != neighbor_word[j]:
                        eliminated_words += 1
            # Store num of eliminated words in neighbor's domain for current word in dict.
            var_domain_n[word] = eliminated_words
        
        # Store list of keys (words) sorted in ascending order based on values (num eliminated words)
        ordered_var_domain = sorted(var_domain_n, reverse=True)

        return ordered_var_domain



    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Return arbitrary unassigned variables
        for var in self.crossword.variables:
            if var not in assignment:
                return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment
        
        # Select unassigned variables
        var = self.select_unassigned_variable(assignment)

        for value in self.domains[var]:
            assignment[var] = value

            # If value consistent with assignment
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
        return None


    def all_arcs(self):
        """
        Return a list of tuples containing pairs of all variables (Arcs) in a crossword.
        """
        arcs = list()
        # For each variable (key) in the domains dict
        for x in self.domains:
            # Check against every other variable
            for y in self.domains:
                if x is y:
                    # If the same variable, skip
                    continue
                else:
                    # Add this the pair of variables to the arcs list
                    arcs.append((x, y))    
        return arcs

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
