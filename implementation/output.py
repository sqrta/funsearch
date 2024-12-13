def priority_v1(term, l, m):
    """Improved version of `priority_v0`."""
    if (
        term[0][0] == "x"
        and term[1][0] == "y"
        and term[2][0] == "y"
        and int(term[1][1]) + int(term[2][1]) == m
    ):
        return True
    if (
        term[0][0] == "x"
        and term[1][0] == "x"
        and term[2][0] == "y"
        and int(term[0][1]) + int(term[1][1]) == l
    ):
        return True
    return False
