class SolverTracker:
    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name

        self.metrics = {
            "algorithm": algorithm_name,
            "steps": 0,
            "assignments": 0,
            "backtracks": 0,
            "domain_reductions": 0,
            "recursive_calls": 0,
            "solved": False,
            "time_taken": 0,
        }

        self.steps = []

    def add_step(self, step_type, cell=None, value=None, message="", extra=None):
        self.metrics["steps"] += 1

        step = {
            "type": step_type,
            "cell": cell,
            "value": value,
            "message": message,
        }

        if extra:
            step.update(extra)

        self.steps.append(step)

    def record_assignment(self, cell, value):
        self.metrics["assignments"] += 1

        row = cell[0] + 1
        col = cell[1] + 1

        self.add_step(
            "assign",
            cell=cell,
            value=value,
            message=f"AI placed {value} in row {row}, column {col} because it satisfies all current Sudoku constraints."
        )

    def record_backtrack(self, cell):
        self.metrics["backtracks"] += 1

        row = cell[0] + 1
        col = cell[1] + 1

        self.add_step(
            "backtrack",
            cell=cell,
            message=f"AI backtracked from row {row}, column {col} because the current path led to a contradiction."
        )

    def record_domain_reduction(self, cell, removed_value):
        self.metrics["domain_reductions"] += 1

        row = cell[0] + 1
        col = cell[1] + 1

        self.add_step(
            "domain_reduction",
            cell=cell,
            value=removed_value,
            message=f"AC3 removed {removed_value} from row {row}, column {col} because it conflicts with neighboring constraints."
        )

    def record_recursive_call(self):
        self.metrics["recursive_calls"] += 1

    def finish(self, solved, time_taken):
        self.metrics["solved"] = solved
        self.metrics["time_taken"] = round(time_taken, 5)

    def get_result(self, board):
        return {
            "solved_board": board,
            "metrics": self.metrics,
            "steps": self.steps,
        }