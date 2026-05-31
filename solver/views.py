from django.shortcuts import render
from django.http import JsonResponse
import json

from .algorithms.backtracking import (
    BacktrackSudokuSolver,
    AC3SudokuSolver,
    AC3LCVSudokuSolver,
    AC3MRVSudokuSolver,
    AC3MRVLCVSudokuSolver,
)


def index(request):
    return render(request, "solver/index.html")


def solve_sudoku(request):
    if request.method == "POST":
        data = json.loads(request.body)

        board = data.get("board")
        algorithm = data.get("algorithm")

        solvers = {
            "backtracking": BacktrackSudokuSolver(),
            "ac3": AC3SudokuSolver(),
            "ac3_lcv": AC3LCVSudokuSolver(),
            "ac3_mrv": AC3MRVSudokuSolver(),
            "ac3_mrv_lcv": AC3MRVLCVSudokuSolver(),
        }

        solver = solvers.get(algorithm)

        if solver is None:
            return JsonResponse({"error": "Invalid algorithm"}, status=400)

        result = solver.solveSudoku(board)
        
        # Limit animation steps so browser does not crash
        result["steps"] = result.get("steps", [])[:800]

        return JsonResponse(result)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)