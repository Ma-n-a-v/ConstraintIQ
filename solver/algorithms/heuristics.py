from random import choice


def count_conflict(csp, variable, value):
    """
    Counts how many neighboring cells still have this value
    in their domain.

    Used for LCV.
    Lower count = less constraining value.
    """
    count = 0

    for neighbor in csp.adjList[variable]:
        if value in csp.domains[neighbor]:
            count += 1

    return count


def order_values_lcv(csp, variable):
    """
    Returns domain values sorted by Least Constraining Value.

    The value that affects fewer neighbors comes first.
    """
    return sorted(
        csp.domains[variable],
        key=lambda value: count_conflict(csp, variable, value)
    )


def select_variable_mrv(csp, uncertain):
    """
    Selects the variable with the smallest domain.

    Used for MRV.
    """
    minimum_index = 0
    minimum_domain_size = float("inf")

    for i, variable in enumerate(uncertain):
        domain_size = len(csp.domains[variable])

        if domain_size < minimum_domain_size:
            minimum_domain_size = domain_size
            minimum_index = i

    uncertain[minimum_index], uncertain[-1] = uncertain[-1], uncertain[minimum_index]

    return uncertain.pop()


def select_variable_mrv_random(csp, uncertain):
    """
    MRV with random tie-breaking.
    Useful when multiple cells have the same smallest domain.
    """
    minimum_size = min(len(csp.domains[var]) for var in uncertain)

    candidates = [
        var for var in uncertain
        if len(csp.domains[var]) == minimum_size
    ]

    selected = choice(candidates)
    uncertain.remove(selected)

    return selected