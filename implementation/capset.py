@funsearch.run
def funcScore():
    score = 0
    for key in allCodes.keys():
        l, m = key
        best = 0
        for code in allCodes[key]:
            if priority(code["A"], l, m):
                r = code["k"] * code["d"] / code["n"]
                if r > best:
                    best = r
        score += best
    return score


@funsearch.evolve
def priority(term, l, m):
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
