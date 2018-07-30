import copy

# Square definitions
X_SQUARE = 'X'
O_SQUARE = 'O'
BLANK = '_'

# Evaluation definitions
X_WINS = 'X wins!'
O_WINS = 'O wins!'
DRAW = 'Draw!'


# Returns true if X's turn to move, false otherwise
def is_X_turn(board):
	x_count = 0
	for row in board:
		x_count += row.count(X_SQUARE)
		x_count -= row.count(O_SQUARE)
	return x_count == 0

# Returns true if every space is taken, false otherwise
def is_full(board):
	for item in board:
		if BLANK in item:
			return False
	return True

# Takes a boardition, and returns a list of every board that can result from a move
def get_moves(board, X_turn):
    symbol = X_SQUARE if X_turn else O_SQUARE
    branches = []    
    for row in range(3):
        for square in range(3):
            if board[row][square] == BLANK:
                branches.append(copy.copy(board))
                branches[-1][row][square] = symbol
    return branches

# Checks for three in a row in the current boardition, returns evaluation
def get_static_eval(board):
    potential_wins = []

	# Three in a row
    for row in board:
        potential_wins.append(set(row))

	# Three in a column
    for i in range(3):
        potential_wins.append(set([board[k][i] for k in range(3)]))

	# Three in a diagonal
    potential_wins.append(set([board[i][i] for i in range(3)]))
    potential_wins.append(set([board[i][2 - i] for i in range(3)]))
    
	# Checking if any three are the same
    for trio in potential_wins:
        if trio == set([X_SQUARE]):
            return X_WINS,board
        elif trio == set([O_SQUARE]):
            return O_WINS,board
    return DRAW

# Dynamically evaluates any valid board move
def do_move(board):
    if len(board) == 9:
        for i in range(len(board)):
            if board[i]==None:
                board[i]='_'
        board=[board[i:i+3] for i in range(0,9,3)]
    
	# Immediately returns static evaluation if it is decisive
    static_eval = get_static_eval(board)
    if static_eval != DRAW:
        return static_eval
    
	# Check for full board
    if is_full(board):
        return DRAW

	# Checking and evaluating every path
    X_turn = is_X_turn(board)
    branches = get_moves(board, X_turn)
    for branch in branches:
        branch_evals= do_move(branch)
        
    outputlist=[]
    outputlist.append(branches)
        
	# Returning the result assuming best play
    if X_turn:
		# X options from best to worst
        if X_WINS in branch_evals:
            return X_WINS,outputlist[-1]
        elif DRAW in branch_evals:
            return DRAW,outputlist[-1]
        else:
            return O_WINS,outputlist[-1]
    else:
		# O options from best to worst
        if O_WINS in branch_evals:
            return O_WINS,outputlist[-1]
        elif DRAW in branch_evals:
            return DRAW,outputlist[-1]
        else:
            return X_WINS,outputlist[-1]


