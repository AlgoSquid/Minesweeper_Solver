def solve_mine(map, n):
    """
    Uses deductive logic to open squares and identify mines. When a state is reached where
    this is not possible, the problem is identified as an (almost) exact cover problem. Thus
    a modified version of Knuth's algorithm X is used to identify the differen possible
    configurations of bomb placements. When more then one configuration is identified and 
    nothing deductive can be derived, the map is deemed unsolvable.
    
    All rights to Ali Assaf: http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
    for the python version of Algorithm X with dancing pairs.
    """
    # Board is initialized and board with bombs discovered for each sqaure is initialized
    board = initialize(map)
    n_bomb = [[0 for y in range(len(board[0]))] for x in range(len(board))]
     
    to_open = set()                       # Squares to open
    to_inspect = set()                    # Squares to inspect for changes
    u = len(board) * len(board[0])        # Number of unopened squares
    
    # Initial zero squares are found and their neighbors are marked to be opened
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "0":
                to_open |= set(find_unopened_neighbors(board, i, j))
                u -= 1
    
    # We loop until there are no more squares to open nor inspect for changes
    initialize_loop = True    # No do-while loop in python
    while to_inspect or to_open or initialize_loop:
        initialize_loop = False
        
        # When no bombs are left, open everything on the board and break
        if n == 0:
            open_everything(board)
            break
        
        # We can mark everything unopened as bombs, when #remaing bombs == #unopened squares
        if u == n:    
            for r in range(len(board)):
                for c in range(len(board[0])):
                    if board[r][c] == "?": board[r][c] = "x"
            break
    
        # As many squares as possible are opened before continuing
        while to_open:
            r, c = to_open.pop()
            n_bomb[r][c] = board[r][c] = str(open(r, c))
            u -= 1
            if board[r][c] is 0:
                # Neighbors can be opened if there are no bombs around this square
                to_open |= set(find_unopened_neighbors(board, r, c))
            else:
                # Bombs are scanned for to disvover possible actions
                updates = scan_for_bombs(board, n_bomb, r, c)
                if "open" in updates: to_open |= set(updates["open"])
                n -= len(updates["update"])
                u -= len(updates["update"])
                updates["update"].append((r, c))
                to_inspect |= set(find_unfinished_neighbors(board, n_bomb, updates["update"]))
        
        # If possible, inspect a square (a neighbor has notified it to rescan)
        if to_inspect:
            r, c = to_inspect.pop()
            updates = scan_for_bombs(board, n_bomb, r, c)
            n, u = update_sets(board, n_bomb, to_open, to_inspect, n, u, updates)
    
        # When no more deductive actions are left, possible configurations of bombs are identified
        if not to_inspect and not to_open and n != 0:
            updates = algorithm_x(board, n_bomb, n, u)
            n, u = update_sets(board, n_bomb, to_open, to_inspect, n, u, updates)
    
    # The proper output board is produced with potential '?' if squares are unsolvable 
    return produce_output(board)

def update_sets(board, n_bomb, to_open, to_inspect, n, u, updates):
    """Updates the different search sets and numeric counters"""
    n -= len(updates["update"])
    u -= len(updates["update"])
    if "open" in updates: to_open |= set(updates["open"])
    to_inspect |= set(find_unfinished_neighbors(board, n_bomb, updates["update"]))
    return n, u

def find_unfinished_neighbors(board, n_bomb, squares):
    """
    Returns a list of squares that have not discovered all their bombs yet 
    and are neighbors to the squares parsed in the 'squares' list.
    """
    unfinished = []
    for row, column in squares:
        for i in range(max(0, row - 1), min(len(board), row + 2)):
            for j in range(max(0, column - 1), min(len(board[0]), column + 2)):
                    if board[i][j].isdigit() and int(board[i][j]) != n_bomb[i][j] and not (i == row and j == column):
                        unfinished.append((i, j))
    return unfinished

def scan_for_bombs(board, n_bomb, row, column):
    """
    Finds and potentially marks bombs and neighbors eligible to be openened.
    Returns a dict of squares to open and squares, whos neighbors should be inspected.
    """
    bombs = 0                        # Bombs discovered
    unopened_neighbors = []          # Unopened neighbors  
    val = int(board[row][column])    # Value of this square (number of bombs for neighbor)
    
    # Bombs are discovered and unopened neighbors are found
    for i in range(max(0, row - 1), min(len(board), row + 2)):
        for j in range(max(0, column - 1), min(len(board[0]), column + 2)):
            if board[i][j] is "x":
                bombs += 1
            elif board[i][j] is "?":
                unopened_neighbors.append((i, j))
    
    # Updates the number of bombs found for this square
    n_bomb[row][column] = bombs
    
    # Squares to open and bombs to mark are found. 
    # "update" are squares that shall notify their neighbors to re-inspect.
    updates = {"update": []}
    if bombs == val:
        # Neighbors can be opened if the required number of bombs are discovered already
        updates["open"] = unopened_neighbors
    elif bombs + len(unopened_neighbors) == val:
        # Bombs can be marked and their neighbors updated
        for r, c in unopened_neighbors:
            board[r][c] = "x"
        updates["update"] = unopened_neighbors
    return updates
        
def find_unopened_neighbors(board, row, column):
    """Returns a list of coordinates for all unopened neighbors of the parsed square"""
    unopened_neighbors = []
    for i in range(max(0, row - 1), min(len(board), row + 2)):
        for j in range(max(0, column - 1), min(len(board[0]), column + 2)):
            if board[i][j] is "?":
                unopened_neighbors.append((i, j))
    return unopened_neighbors

def open_everything(board):
    """Opens all unopened squares on the board"""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] is "?":
                board[r][c] = str(open(r, c))

def algorithm_x(board, n_bomb, n, u):
    """
    Identifies ALL possible configurations of bombs with the knowledge available
    using Knuth's Algorithm X with dancing pairs - now Python dict style.
    Configurations are filtered, so only feasible configurations are accepted.
    If two feasible configurations are possible, then nothing will returned and
    the entire algorithm terminate with a "?".
    """
    unfinished = dict()      # All opened squares that have not discovered all their bomb neighbors
    unopened = dict()        # All unopened sqaures that are neighbors to the identified unfinished ones
    undiscovered = dict()    # Number of undiscovered bombs for each unfinished square
    
    # The 3 dicts are populated, such that an unfinished square has a list of all its unopened neighbors
    # and an unopened square has a list of all its unfinished neighbors.
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c].isdigit() and int(board[r][c]) != n_bomb[r][c]:
                unopened_neighbors = find_unopened_neighbors(board, r, c)
                unfinished[(r, c)] = set(unopened_neighbors)
                undiscovered[(r, c)] = int(board[r][c]) - n_bomb[r][c]
                for neighbor in unopened_neighbors:
                    if neighbor in unopened:
                        unopened[neighbor].append((r, c))
                    else:
                        unopened[neighbor] = [(r, c)]
    
    # All configurations of bomb placements are returned.
    bomb_lists = search(unfinished, unopened, undiscovered, [], [])
    
    # Configurations are filtered for validation.
    temp_list = []
    for bombs in bomb_lists:
        if u > len(unopened) and len(bombs) <= n:
            temp_list.append(bombs)
        elif u == len(unopened) and len(bombs) == n:
            temp_list.append(bombs)
    bomb_lists = temp_list
    
    if len(bomb_lists) == 0:
        # No valid configuration found.
        return {"update": []}
    elif len(bomb_lists) == 1:
        # A single configuration found and we mark all identified bombs.
        for r, c in bomb_lists[0]:
            board[r][c] = "x"
        return {"update": bomb_lists[0]}
    else:
        # Multiple valid configurations found and we look for insections between configurations
        # and squares which we know for sure are cannot be bombs.
        intersection = set(bomb_lists[0])
        for bombs in bomb_lists:
            intersection = intersection & set(bombs)
            for bomb in bombs:
                unopened.pop(bomb, None)
        updates = {"update": []}
        if unopened:
            updates["open"] = unopened.keys()
        if intersection:
            for r, c in list(intersection):
                board[r][c] = "x"
            updates["update"] = intersection
        return updates

def search(X, Y, Z, solution, solutions):
    """Recursive selection and deselction of rows and columns matched"""
    if not X:
        # A path in the search tree has been identified and the solution is saved 
        solution_copy = []
        for r, c in solution:
            solution_copy.append((r, c))
        solutions.append(solution_copy)
    else:
        # We always choose the lowest number of rows for a column
        c = min(X, key=lambda c: len(X[c]))    
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, Z, r)
            search(X, Y, Z, solution, solutions)
            deselect(X, Y, Z, r, cols)
            solution.pop()
    return solutions

def select(X, Y, Z, r):
    """
    Selects a row and thus removes the matched columns.
    If a column should be matched multiple times, it's only subtracted.
    """
    cols = [], []
    for j in Y[r]:
        Z[j] -= 1
        if Z[j] == 0:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols[0].append(X.pop(j))
        else:
            cols[1].append(j)
    return cols

def deselect(X, Y, Z, r, cols):
    """
    A row is deslected and thus previous matched columns are released.
    The column is only released if we are sure that it was fully removed.
    """
    for j in reversed(Y[r]):
        Z[j] += 1
        if Z[j] == 1:
            X[j] = cols[0].pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

def initialize(map):
    """Returns a proper 2-dimensional list of the map"""
    # Dimensions are found
    rows = map.count("\n") + 1
    columns = int((len(map) + 1)  / (rows * 2))
    dim = [rows, columns]
    
    # 2-dimensional board is created with the specified dimensions
    board = [[" " for y in range(dim[1])] for x in range(dim[0])]
    
    # Values are inserted into the board
    for i in range(dim[0]):
        for j in range(dim[1]):
            board[i][j] = map[i * (dim[1] * 2) + j * 2]
    return board

def produce_output(board):
    """Creates the output format from the board"""
    output = ""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] is "?": return "?"
            output += board[i][j] + " " if j < len(board[0]) - 1 else board[i][j]
        output += "\n" if i < len(board) - 1 else ""
    return output
