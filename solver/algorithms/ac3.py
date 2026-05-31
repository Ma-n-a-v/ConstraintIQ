from collections import defaultdict
'''
AC-3

This code snippet implements the AC-3 (Arc Consistency Algorithm 3) for enforcing arc consistency in Constraint Satisfaction Problems (CSPs). 
The purpose of AC-3 is to reduce the search space by pruning values from variables' domains that are inconsistent with the constraints, thus potentially simplifying the CSP to a point where it can be solved more easily, or determining that no solution exists if a domain becomes empty.

`remove_inconsistent_values` Function:
- Purpose: Checks and removes values from the domain of a variable `Xt` that are inconsistent with another variable `Xh`.
- Process:
    - Iterates through each possible value `x` in the domain of `Xt`. For each `x`, it checks if there exists at least one value `y` in the domain of `Xh` such that `Xt=x` does not conflict with `Xh=y` based on the constraints defined in `csp.conflicts`.
    - If `x` conflicts with every possible `y`, `x` is removed from `Xt`'s domain, and this removal is recorded in removals.
    - Returns True if any value was removed, indicating the domain of `Xt` was revised.
    
    
`AC3` Function:
- Purpose: Establishes arc consistency for the entire CSP.
- Initialization:
    - If no queue of arcs is provided, it initializes the queue with all arcs in the CSP, represented as pairs of variables (Xt, Xh) where Xt and Xh have a constraint between them.
- Process:
    - Continuously processes each arc (Xt, Xh) in the queue. For each arc, it calls remove_inconsistent_values to potentially prune the domain of Xt.
    - If any value was removed (domain revised), it checks:
        - If `Xt`'s domain is empty, returns False, indicating no consistent assignment is possible.
        - Otherwise, it enqueues all arcs `(X, Xt)` for neighboring variables `X` of `Xt`, excluding the back arc to `Xh`, to recheck consistency due to the domain change in `Xt`.
- Outcome:
    - Returns `True` if arc consistency is achieved across all variables without emptying any domain, indicating a potential path towards a solution.
    - Returns `False` if any variable's domain is emptied, indicating no solution is possible under current constraints.
    
`makeArcQue` Function:
- Generates a queue of arcs given a subset of variables `Xs`. For each variable `Xh` in `Xs`, it pairs `Xh` with every variable `Xt` that is adjacent to `Xh` (as determined by the CSP's adjacency list).
- This function is useful for initializing the AC3 algorithm with a specific set of arcs, possibly focusing on parts of the CSP that were recently modified or are of particular interest.
- The resulting queue can be used to apply arc consistency checks to a targeted subset of the CSP's variables, which can be efficient in dynamic or incremental settings where only part of the CSP changes or requires reevaluation.
'''

def remove_inconsistent_values(csp, Xt, Xh, removals, tracker=None):
    # Return True if we remove a value
    revised = False
    # If Xt=x conflicts with Xh=y for every possible y, eliminate Xt=x
    for x in csp.domains[Xt].copy():
        for y in csp.domains[Xh]:
            if not csp.conflicts(*Xt, x, *Xh, y):
                break
        else:
            csp.domains[Xt].remove(x)
            removals[Xt].add(x)
            revised = True
            if tracker:
                tracker.record_domain_reduction(
                    cell=[Xt[0], Xt[1]],
                    removed_value=x + 1
                )
    return revised


def AC3(csp, queue=None, removals=None, tracker=None):
    if removals is None:
        removals = defaultdict(set)
        
    # Return False if there is no consistent assignment
    if queue is None:
        queue = [(Xt, X) for Xt in csp.adjList for X in csp.adjList[Xt]]
    # Queue of arcs of our concern
    while queue:
        # Xt --> Xh Delete from domain of Xt
        (Xt, Xh) = queue.pop()
        if remove_inconsistent_values(csp, Xt, Xh, removals, tracker):
            if not csp.domains[Xt]:
                return False
            # NOTE: Next two lines only for binary "!=" constraint
            elif len(csp.domains[Xt]) > 1:
                continue
            for X in csp.adjList[Xt]:
                if X != Xt:
                    queue.append((X, Xt))
    return True

def makeArcQue(csp, Xs):
    return [(Xt, Xh) for Xh in Xs for Xt in csp.adjList[Xh]]
