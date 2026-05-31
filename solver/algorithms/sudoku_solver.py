from collections import defaultdict
'''
The `CSP` class is designed to represent a constraint satisfaction problem. 
It is initialized with three key attributes:
    1. `variables`: A list of variables involved in the CSP.
    2. `adjList`: An adjacency list representing the constraints between variables; essentially, it maps each variable to a list of variables that have constraints with it.
    3. `domains`: A dictionary mapping each variable to its domain, which is the set of values that the variable can take.

The `restore_domains` method undoes a supposition and all inferences from it. 
This is used when backtracking in the CSP solution process. 
It takes a dictionary of removals where keys are variables and values are the set of values that were removed from these variables' domains. 
It then restores these values to the domains.

The `conflicted_vars` method returns a list of variables that are in conflict in the current assignment. 
It iterates through all variables and includes those for which `nconflicts` with their currently assigned value and the current assignment is greater than 0, indicating at least one conflict.
'''
class CSP(object):
    def __init__(self, variables = [], adjList = {}, domains = {}):
        self.variables = variables
        self.adjList = adjList
        self.domains = domains

    def restore_domains(self, removals):
        """ Undo a supposition and all inferences from it """
        for X in removals:
            self.domains[X] |= removals[X]

    #the following methods are used in min_conflict algorithm
    def nconflicts(self, X1, x, assignment):
        """
        Return the number of conflicts X1 = x has with other variables
        Subclasses may implement this more efficiently
        """
        def conflict(X2):
            return self.conflicts(X1, x, X2, assignment[X2])
        return sum(conflict(X2) for X2 in self.adjList[X1] if X2 in assignment)

    def conflicted_vars(self, current):
        """ Return a list of variables in conflict in current assignment """
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]
        
        
'''
Class Definition: SudokuCSP

Inherits from the `CSP` class to leverage the generic CSP infrastructure such as variables, domains, adjacency lists, and basic CSP operations. 
It is specialized to handle the specific constraint checking needed for Sudoku puzzles.

The `conflicts` method takes six parameters: `(i1, j1, x, i2, j2, y)`, where 
    `i1, j1` and `i2, j2` are the row and column indices of two cells in the Sudoku grid, 
    and `x` and `y` are the values assigned to these cells, respectively. 
    
    The method calculates `k1` and `k2`, which are the indices of the 3x3 subgrids (also known as boxes or blocks) that contain the cells `(i1, j1)` and `(i2, j2)`. 
    This calculation divides the grid into 3x3 sections and assigns a unique index to each.

It then returns `True` if the assigned values `x` and `y` are equal and at least one of the following conditions is met:
- `i1 == i2`: The two cells are in the same row.
- `j1 == j2`: The two cells are in the same column.
- `k1 == k2`: The two cells are in the same 3x3 subgrid.

If any of these conditions is true, it means that the assignment of `x` to `(i1, j1)` and `y` to `(i2, j2)` violates the Sudoku rules,
which state that each number 1-9 must appear exactly once in each row, each column, and each of the nine 3x3 subgrids.

This customized `conflicts` method allows the `SudokuCSP` class to directly support the validation of Sudoku constraints. 
It effectively checks whether two assignments conflict based on the Sudoku rules. 
This is a key component in solving Sudoku puzzles using CSP techniques, as it enables the identification and resolution of constraint violations.

By extending the `CSP` class, `SudokuCSP` can utilize the broader CSP-solving mechanisms (like backtracking, constraint propagation, and heuristics) 
while applying these specifically tailored constraint checks to ensure any proposed solution adheres to the Sudoku rules.
'''

class SudokuCSP(CSP):
    def conflicts(self, i1, j1, x, i2, j2, y):
        k1 = i1 // 3 * 3 + j1 // 3
        k2 = i2 // 3 * 3 + j2 // 3
        return x == y and ( i1 == i2 or j1 == j2 or k1 == k2 )
    
    
    
    
    
'''
Class Definition: SudokuSolver

The `__addEdge__` method is intended to construct adjacency lists that define the constraints between different cells in the Sudoku board. 
It takes the row (`i`) and column (`j`) of a cell, along with an existing adjacency list (adjList), and updates the adjacency list to include all cells that are in the same row, column, or 3x3 subgrid as the given cell, except the cell itself. 
It calculates `k`, the index of the 3x3 subgrid to which the cell belongs, and iterates through all possible row and column indices (0 to 8) to add constraints. 
The method ensures that each cell is related to others that must have a different value according to Sudoku rules.

The `buildCspProblem` method initializes the CSP framework for solving a Sudoku puzzle. 
It creates an adjacency list (adjList), a list of variables (variables), a list of assigned variables (assigned), and domains (domains) for each cell. 
It uses `__addEdge__` to populate adjList with constraints based on the rules of Sudoku. 
For each cell, if the cell is empty (denoted by `.`), its domain is set to all possible values (1 through 9, adjusted to 0 through 8 to fit Python's 0-indexed nature). 
If a cell is already filled with a number, its domain is set to that specific number, and it's added to the list of assigned variables. 
The method returns an instance of SudokuCSP, initialized with the variables, adjacency list, and domains, along with a list of already assigned variables.

The `solveSudoku` method is intended to be the main function that takes a Sudoku board as input and solves it. 
The board is represented as a list of lists of strings (or for the django application the div), where each string can be a digit ('1' to '9') or '.' for empty cells.
The actual solving logic (CSP solving technique, backtracking, etc.) would be implemented within this method or called from this method. 
The placeholder pass indicates that the solving functionality is to be implemented.
'''
    
class SudokuSolver(object):
    def __addEdge__(self, i, j, adjList):
        k = i // 3 * 3 + j // 3
        for num in range(9):
            if num != i:
                adjList[(i, j)].add((num, j))
            if num != j:
                adjList[(i, j)].add((i, num))
            row = num//3 + k//3 * 3
            col = num%3 + k%3 * 3
            if row != i or col != j:
                adjList[(i, j)].add((row, col))

    def buildCspProblem(self, board):
        adjList = defaultdict(set)
        # Build graph (contraints)
        for i in range(9):
            for j in range(9):
                self.__addEdge__(i, j, adjList)
        # Set domains
        variables = []
        assigned = []
        domains = {}
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    domains[(i, j)] = set(range(9))
                    variables.append((i, j))
                else:
                    domains[(i, j)] = set([int(board[i][j]) - 1])
                    assigned.append((i, j))
        return SudokuCSP(variables, adjList, domains), assigned

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        pass