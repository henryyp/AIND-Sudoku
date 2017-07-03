# ROWS AND COL identifier
rows = 'ABCDEFGHI'
cols = '123456789'


assignments = []

# ASSIGN VALUES
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())

    return values


# CORSS
def cross(A, B):
    return [s+t for s in A for t in B]


# UTILS FUNC VARS
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# build diagonal list
diag1_units = [r+cols[i] for i, r in enumerate(rows)]
diag2_units = [r+cols[len(cols) - 1 - i] for i, r in enumerate(rows)]
diag_units = [diag1_units, diag2_units]

simpleUnitlist = row_units + column_units + square_units
unitlist = row_units + column_units + square_units + diag_units
simpleUnits = dict((s, [u for u in simpleUnitlist if s in u]) for s in boxes)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


# GRID VALUES
def grid_values(grid):
    len(grid) == 81
    return dict(zip(boxes, map(lambda num: '123456789' if num == '.' else num, grid)))


# ELIMINATE
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
    return values


# ONLY CHOICE
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

# NAKED TWINS
def naked_twins(values):

    for unit in simpleUnitlist:
        # FIND twins boxes
        l = [values[box] for box in unit if len(values[box]) == 2]
        # filter out repeating twin boxes
        nakedTwinVal = list(set([ x for x in l if l.count(x) == 2 ]))

        for box2 in unit:
            for val in nakedTwinVal:
                if values[box2] != val and len(val) > 0:
                    replaceWith = list(set(values[box2]) - set(val))
                    replaceWith.sort()
                    assign_value(values, box2, ''.join(replaceWith))

    return values


# REDUCE WITH THE 3 Constraint propogation techniques
def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


# SEARCH
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


# DISPLAY
def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


# SOLVE AND DISPLAY IT!
def solve(grid):
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
