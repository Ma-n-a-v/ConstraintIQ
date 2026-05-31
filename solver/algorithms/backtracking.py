from .sudoku_solver import SudokuSolver
from .ac3 import AC3, makeArcQue
from collections import defaultdict
from random import choice
from .metrics import SolverTracker
import time

def _cell_tuple_to_list(cell):
    return [cell[0], cell[1]]


def _build_uncertain_cells(csp):
    uncertain = []

    for i in range(9):
        for j in range(9):
            if len(csp.domains[(i, j)]) > 1:
                uncertain.append((i, j))

    return uncertain


def _fill_board_from_domains(board, csp):
    for i in range(9):
        for j in range(9):
            if board[i][j] == ".":
                assert len(csp.domains[(i, j)]) == 1
                board[i][j] = str(next(iter(csp.domains[(i, j)])) + 1)

'''
> Class Definition: BacktrackSudokuSolver

The `BacktrackSudokuSolver` class extends SudokuSolver to solve Sudoku puzzles using a backtracking algorithm.

`heng`, `zong`, and `gezi` are lists of sets, each corresponding to rows, columns, and 3x3 squares (grids) of the Sudoku board, respectively. 
These sets track the numbers already used in each row, column, and grid. 
`blank` is a list to store the positions `(i, j)` of all the empty cells `('.')` in the Sudoku board.
The class iterates over the entire 9x9 Sudoku board. For each cell, if it contains a number (not `'.'`), the number (adjusted by -1 for 0-indexing) is added to the corresponding row, column, and grid sets. 
This step initializes the tracking structures with the given numbers in the puzzle. 
If the cell is empty (`'.'`), its position is added to blank for further processing.

> The `backtrack` Function:
- A recursive function designed to try filling all empty cells with valid numbers.
- `start` is the index in blank to start the backtracking from.
- For each empty cell, identified by its position `(i, j)` from `blank`, the function tries numbers 0 through 8 (which correspond to Sudoku numbers 1 through 9).
- It checks if the current number is not already used in the same row (`heng[i]`), column (`zong[j]`), or grid (`gezi[k]`). If not, it places the number in the cell and recursively calls itself to try filling the next empty cell.
- If placing a number leads to a dead end (no valid number can be placed in the next empty cell(s)), it removes the number from the cell and the tracking sets, and tries the next number.
- The recursion base case is when start exceeds the number of empty cells, meaning the board is successfully filled. It returns True to signal success.


> Solving the Sudoku:
The `solveSudoku` method initializes the tracking structures and calls `backtrack(0)` to start solving the puzzle from the first empty cell.
Since the solution modifies the `board` in place, no return value is necessary. 
The return None at the end is optional since Python functions return `None` by default if no return statement is executed.
'''

class BacktrackSudokuSolver(SudokuSolver):
    def solveSudoku(self, board):
        tracker = SolverTracker("Backtracking")
        start_time = time.time()

        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        blanks = []

        for i in range(9):
            for j in range(9):
                if board[i][j] != ".":
                    box_index = i // 3 * 3 + j // 3
                    num = int(board[i][j]) - 1

                    rows[i].add(num)
                    cols[j].add(num)
                    boxes[box_index].add(num)
                else:
                    blanks.append((i, j))

        def backtrack(start):
            tracker.record_recursive_call()

            if start >= len(blanks):
                return True

            i, j = blanks[start]
            box_index = i // 3 * 3 + j // 3

            tracker.add_step(
                "select_cell",
                cell=[i, j],
                message=f"AI selected row {i + 1}, column {j + 1} as the next empty cell to evaluate."
            )

            for num in range(9):
                if num not in rows[i] and num not in cols[j] and num not in boxes[box_index]:
                    value = str(num + 1)

                    board[i][j] = value
                    rows[i].add(num)
                    cols[j].add(num)
                    boxes[box_index].add(num)

                    tracker.record_assignment([i, j], value)

                    if backtrack(start + 1):
                        return True

                    rows[i].remove(num)
                    cols[j].remove(num)
                    boxes[box_index].remove(num)
                    board[i][j] = "."

                    tracker.record_backtrack([i, j])

            return False

        solved = backtrack(0)
        tracker.finish(solved, time.time() - start_time)

        return tracker.get_result(board)



'''
class: AC3SudokuSolver

The code defines a class `AC3SudokuSolver` that extends `SudokuSolver` to solve Sudoku puzzles by integrating backtracking search with the AC3 algorithm for maintaining arc consistency.

Here's an outline of how the solution process is implemented:

> Building the CSP Problem:
- The method `solveSudoku` starts by constructing the CSP model of the given Sudoku puzzle using the inherited `buildCspProblem` method, which sets up the variables, domains, and constraints (adjacency list) based on the initial board state.
- `assigned` captures the initially filled cells of the Sudoku board, which are treated as variables with a fixed domain (the given value).


> Applying AC3:
- The AC3 algorithm is applied to enforce arc consistency across the entire problem space, using `makeArcQue` to generate the queue of arcs from the initially assigned variables. This step aims to reduce the domains of variables by eliminating values that cannot participate in any valid solution, based on the current constraints.

> Identifying Uncertain Choices:
- The solver identifies cells (variables) with uncertain values—those whose domains contain more than one possible value—after the initial application of AC3. These cells are added to the `uncertain` list for further exploration through backtracking.

> Backtracking Search:
- The `backtrack` method is recursively called to explore different value assignments for the uncertain cells in an attempt to find a valid solution.
- For each uncertain cell `X`, the method iterates over all possible values `x` in its domain. For each `x`, it temporarily assigns `x` to `X`, updates the CSP model accordingly, and applies AC3 again to propagate the effects of this assignment.
- If AC3 indicates a consistent assignment is still possible (i.e., no domain is emptied), the search continues recursively with the next uncertain cell. If a solution is found (`retval` is `True`), the recursion unwinds successfully.
- If no valid assignment is found for `X`, the changes are undone (`csp.restore_domains`), and the method tries the next value of `X`.
- The uncertain cell `X` is added back to the list of uncertain cells if no solution is found with `X` being assigned any of its possible values.

> Updating the Original Board:
- Once a valid solution is found (all `uncertain` cells are successfully assigned), the method updates the original `board` with the solved values, converting them from 0-indexed to 1-indexed format (`csp.domains[(i, j)].pop() + 1`).

'''
# Backtracking search with AC3 Maintaining Arc Consistency
class AC3SudokuSolver(SudokuSolver):
    algorithm_name = "AC3 + Backtracking"

    def solveSudoku(self, board):
        tracker = SolverTracker(self.algorithm_name)
        start_time = time.time()

        csp, assigned = self.buildCspProblem(board)

        if not AC3(csp, makeArcQue(csp, assigned), tracker=tracker):
            tracker.finish(False, time.time() - start_time)
            return tracker.get_result(board)

        uncertain = _build_uncertain_cells(csp)

        solved = self.backtrack(csp, uncertain, tracker)

        if solved:
            _fill_board_from_domains(board, csp)

        tracker.finish(solved, time.time() - start_time)

        return tracker.get_result(board)

    def select_variable(self, csp, uncertain, tracker):
        variable = uncertain.pop()

        tracker.add_step(
            "select_cell",
            cell=_cell_tuple_to_list(variable),
           message=f"AI selected row {variable[0] + 1}, column {variable[1] + 1} using the default search ordering strategy."
        )

        return variable

    def order_values(self, csp, variable, tracker):
        return list(csp.domains[variable])

    def backtrack(self, csp, uncertain, tracker):
        tracker.record_recursive_call()

        if not uncertain:
            return True

        variable = self.select_variable(csp, uncertain, tracker)
        original_domain = csp.domains[variable].copy()
        values = self.order_values(csp, variable, tracker)

        for value in values:
            removals = defaultdict(set)

            for domain_value in original_domain:
                if domain_value != value:
                    removals[variable].add(domain_value)

            csp.domains[variable] = {value}

            tracker.record_assignment(
                _cell_tuple_to_list(variable),
                value + 1
            )

            success = AC3(
                csp,
                makeArcQue(csp, [variable]),
                removals,
                tracker=tracker
            )

            if success:
                if self.backtrack(csp, uncertain, tracker):
                    return True

            csp.restore_domains(removals)
            csp.domains[variable] = original_domain.copy()

            tracker.record_backtrack(_cell_tuple_to_list(variable))

        uncertain.append(variable)
        return False
        



'''
Class: AC3LCVSudokuSolver

The code outlines an extension of the `AC3SudokuSolver`, creating a new class called `AC3LCVSudokuSolver`, which integrates the Least Constraining Value (LCV) heuristic into the backtracking search process.
The LCV heuristic aims to choose the value that imposes the fewest constraints on the remaining unassigned variables, thereby potentially reducing the search space and leading to faster solutions. 

Let's break down the modifications and additions:

> `count_conflict` Method:

- This method calculates the number of conflicts a potential value `x` for a variable `Xi` would have with its adjacent variables according to the CSP's adjacency list. A conflict here means that the value `x` is present in the domain of an adjacent variable `X`.
- The `cnt` (count) represents how constraining the value `x` is if assigned to `Xi`. The fewer conflicts (`cnt`), the less constraining the value is considered.

> Modified `backtrack` Method:
- The `backtrack` method is overridden to incorporate the LCV heuristic into the value selection process for each uncertain variable.
- When selecting a value for variable `X` from its domain, the values are first sorted based on how many conflicts they generate with adjacent variables, as determined by the `count_conflict` method. This sorting orders the values from least to most constraining (Least Constraining Value).
- The search then proceeds by attempting to assign values to `X` in the order of least constraining to most constraining. This is done in the hope that choosing values that are less likely to constrain the domains of other variables will lead to fewer backtracks and a quicker solution.
- The rest of the `backtrack` method remains largely the same as in the base `AC3SudokuSolver`. It temporarily assigns a value `x` to `X`, applies AC3 to enforce arc consistency, and recursively continues the search. If no solution is found with `x`, the changes are undone, and the next least constraining value is tried.
- If all values for `X` are tried without success, `X` is added back to the list of uncertain variables, and the method backtracks.

> Outcome and Efficiency:
- By prioritizing the assignment of values that are least constraining to other variables, the `AC3LCVSudokuSolver` aims to navigate the search space more effectively than a straightforward backtracking approach. The LCV heuristic helps in minimizing the chance of future conflicts, thereby potentially reducing the number of backtracks needed to find a solution.
- The combination of AC3 for reducing the domain sizes through arc consistency and the LCV heuristic for intelligent value ordering makes this solver particularly adept at tackling complex Sudoku puzzles with efficiency.

'''
# AC3 filtering with Least Constraining Value ordering
class AC3LCVSudokuSolver(AC3SudokuSolver):
    algorithm_name = "AC3 + LCV"

    def count_conflict(self, csp, variable, value):
        count = 0

        for neighbor in csp.adjList[variable]:
            if value in csp.domains[neighbor]:
                count += 1

        return count

    def order_values(self, csp, variable, tracker):
        values = sorted(
            csp.domains[variable],
            key=lambda value: self.count_conflict(csp, variable, value)
        )

        tracker.add_step(
            "lcv_order",
            cell=_cell_tuple_to_list(variable),
            message=f"LCV prioritized values for row {variable[0] + 1}, column {variable[1] + 1} from least restrictive to most restrictive.",
            extra={
                "ordered_values": [value + 1 for value in values]
            }
        )

        return values
    
    
'''
Class: AC3MRVSudokuSolver

The `AC3MRVSudokuSolver` class extends the `AC3SudokuSolver` to solve Sudoku puzzles by incorporating the Minimum Remaining Values (MRV) heuristic into the backtracking search process. 
MRV selects the variable with the fewest legal values left in its domain to assign next, potentially reducing the search space and increasing efficiency. 
Let's explore the functionalities added and modified in this solver:

> Modified `solveSudoku` Method:
- This method builds the CSP model from the given Sudoku board, applies AC3 to enforce arc consistency from the start, identifies uncertain cells (those with more than one possible value left), and then proceeds with backtracking search to find a solution.
- After finding a solution, it updates the original Sudoku board with the solved values.

> `popMinRandom` and `popMin` Methods:
- `popMinRandom` and `popMin` are utility methods designed to select and remove a variable from the `uncertain` list based on the MRV heuristic. While both methods aim to select the variable with the minimum number of legal values (minimum domain size), `popMinRandom` introduces randomness when there are multiple variables with the same smallest domain size by randomly choosing one of them. This could potentially provide a diversity of search paths in repeated runs. `popMin`, on the other hand, consistently chooses the first variable it finds with the minimum domain size.
- These methods rearrange the selected variable to the end of the array and then pop it, optimizing the removal process.

> Modified backtrack Method:
- Overrides the `backtrack` method from `AC3SudokuSolver` to integrate the MRV heuristic explicitly. Instead of popping the last item from `uncertain`, it uses `popMin` to select the next variable to assign based on MRV, aiming to reduce branching in the search tree.
- For each chosen variable `X`, it iterates over all possible values `x` in its domain, temporarily assigns `x` to `X`, and applies AC3 to propagate constraints and possibly reduce the domains of other variables further.
- If a consistent assignment is found (AC3 returns True), it recursively continues with the next variable. If the assignment leads to a dead-end, it restores the previous state and tries the next value.
- If all values for `X` are exhausted without success, `X` is added back to the list of uncertain variables for potential reassignment, and the method backtracks.

> Key Features:
- The integration of the MRV heuristic aims to choose the most constrained variable (the one with the fewest legal moves) as the next variable to assign, theoretically minimizing the number of decisions and backtracks needed.
- The MRV heuristic is particularly effective in constraint-dense problems like Sudoku, where early decisions significantly influence the complexity of remaining decisions.
- The `AC3MRVSudokuSolver` leverages both arc consistency (via AC3) to reduce domain sizes before and during search, and MRV to intelligently select the next variable to assign, aiming for a more efficient search process.
'''
# AC3 filtering with Minimum Remaining Values ordering
class AC3MRVSudokuSolver(AC3SudokuSolver):
    algorithm_name = "AC3 + MRV"

    def popMinRandom(self, array, key):
        minimum = float("inf")
        indices = []

        for i in range(len(array)):
            value = key(array[i])

            if value < minimum:
                indices = [i]
                minimum = value
            elif value == minimum:
                indices.append(i)

        index = choice(indices)
        array[index], array[-1] = array[-1], array[index]
        return array.pop()

    def popMin(self, array, key):
        minimum = float("inf")
        index = 0

        for i in range(len(array)):
            value = key(array[i])

            if value < minimum:
                index = i
                minimum = value

        array[index], array[-1] = array[-1], array[index]
        return array.pop()

    def select_variable(self, csp, uncertain, tracker):
        variable = self.popMin(
            uncertain,
            lambda cell: len(csp.domains[cell])
        )

        tracker.add_step(
            "mrv_select",
            cell=_cell_tuple_to_list(variable),
            message=f"MRV selected row {variable[0] + 1}, column {variable[1] + 1} because it has only {len(csp.domains[variable])} legal value(s) remaining."        )

        return variable


'''
Class: AC3MRVLCVSudokuSolver

The `AC3MRVLCVSudokuSolver` class extends `AC3SudokuSolver` to incorporate both the MRV heuristic and the LCV heuristic into the Sudoku solving process. 
This combination aims to further optimize the backtracking search by intelligently selecting which variable to assign next (MRV) and in what order to try the possible values for that variable (LCV). 

Here's an in-depth look at how the class implements these strategies:

> Integrating MRV and LCV:
- MRV (Minimum Remaining Values): This heuristic selects the next variable to assign by choosing the one with the fewest legal (remaining) values in its domain. The idea is that variables with fewer options are more constrained and thus should be assigned earlier to reduce the branching factor in the search tree.
- LCV (Least Constraining Value): Once a variable is selected for assignment (using MRV), the LCV heuristic orders the values in its domain based on how many options they leave open for the adjacent variables (i.e., how constraining they are to the rest of the variables in the CSP). The value that leaves the most options available (least constraining) is tried first.

> Key Methods:
- `count_conflict`: Counts how many times a potential value for a variable appears in the domains of adjacent variables. It's used for the LCV heuristic to determine how constraining a value is.
- `popMin`: Extracts the variable with the minimum domain size from the list of uncertain variables, applying the MRV heuristic. It modifies the input list in place and returns the selected variable.
- `solveSudoku`:
    - Builds the CSP model from the Sudoku board.
    - Applies AC3 to enforce arc consistency, reducing the domains of variables before starting the search.
    - Identifies uncertain variables (those with domains larger than one value) and attempts to solve the CSP using backtracking.
    - If a solution is found, updates the original board with the solved values.
- `backtrack`:
    - Applies MRV to select the next variable to assign by using `popMin`.
    - Orders the values in the selected variable's domain according to LCV by sorting them based on the `count_conflict` measure.
    - Tries each value in order, setting the variable to that value and recursively attempting to solve the rest of the puzzle.
    - Uses AC3 after each assignment to maintain arc consistency, potentially reducing the domains of other variables based on the new assignment.
    - Restores previous domains if a value leads to a dead end, using `restore_domains`.
    - If no values lead to a solution for the current variable, adds the variable back to the list of uncertain variables and backtracks.

> Outcome:
By combining MRV and LCV, the `AC3MRVLCVSudokuSolver` aims to significantly improve the efficiency of solving Sudoku puzzles compared to using backtracking alone. 
The MRV heuristic helps reduce the size of the search tree by focusing on the most constrained variables first, while the LCV heuristic aims to minimize the impact of each assignment on the rest of the puzzle, ideally leading to fewer conflicts and backtracks. 
This dual heuristic approach, combined with arc consistency checks (AC3), makes for a powerful and efficient Sudoku solving strategy.
'''
# AC3 filtering with Minimum Remaining Values and Least Constraining Value
class AC3MRVLCVSudokuSolver(AC3MRVSudokuSolver):
    algorithm_name = "AC3 + MRV + LCV"

    def count_conflict(self, csp, variable, value):
        count = 0

        for neighbor in csp.adjList[variable]:
            if value in csp.domains[neighbor]:
                count += 1

        return count

    def order_values(self, csp, variable, tracker):
        values = sorted(
            csp.domains[variable],
            key=lambda value: self.count_conflict(csp, variable, value)
        )

        tracker.add_step(
            "lcv_order",
            cell=_cell_tuple_to_list(variable),
            message=f"LCV ordered values for cell ({variable[0] + 1}, {variable[1] + 1}).",
            extra={
                "ordered_values": [value + 1 for value in values]
            }
        )

        return values
