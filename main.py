import sys
# Check Move
def check_king(position):
    moves_list = []
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0),
               (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def check_queen(position):
    moves_list = check_bishop(position)
    second_list = check_rook(position)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

def check_bishop(position):
    moves_list = []
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                chain += 1
            else:
                path = False
    return moves_list

def check_rook(position):
    moves_list = []
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                chain += 1
            else:
                path = False
    return moves_list

def check_pawn(position):
    moves_list = []
    moves_list.append((position[0] -1, position[1]-1 ))
    moves_list.append((position[0] -1, position[1]+1 ))
    return moves_list

# Manage Board
def string_to_board(multi_line_string):
    lines = multi_line_string.strip().split('\n')  # Remove leading/trailing whitespace
    board = []
    for line in lines:
        row = line.split()
        if len(row) > 8:
            print("Error: The board is too large.")
            return -1  # Unequal row length
        board.append(row)  # Split line by whitespace to remove spaces
    
    row_lengths = [len(line.split()) for line in lines]
    if len(set(row_lengths)) != 1:
        print("Error: Unequal row lengths")
        return -1  # Unequal row lengths

    return board

def read_board_from_file(filename):
    with open(filename, 'r') as file:
        board_string = file.read()
    return board_string

def create_base(num_rows, num_cols):
    return [['.' for _ in range(num_cols)] for _ in range(num_rows)]

# Calculate
def count_rows_cols(board):
    num_rows = len(board)
    if num_rows == 0:
        return 0, 0  # Empty board
    
    num_cols = len(board[0])
    return num_rows, num_cols

def find_characters(board):
    characters = {}
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col not in characters:
                characters[col] = []
            characters[col].append((i, j))
    return characters

def is_king_checked(board, king_position):
    characters = find_characters(board)
    attacking_pieces = []
    for char, positions in characters.items():
        if char != 'K':
            for pos in positions:
                if king_position in get_valid_moves(board, pos):
                    attacking_pieces.append((char, pos))
    if attacking_pieces:
        print("\nSuccess")
        name = {
            'K':'King',
            'Q':'Queen',
            'P':'Pawn',
            'B':'Bishop',
            'R':'Rook'
        }
        for char, pos in attacking_pieces:
            print(f"\n{name[char]} ({char}):")
            draw_moves(base,char,pos)
        return True
    else:
        print("\nFail")
        return False

def get_valid_moves(board, position):
    char = board[position[0]][position[1]]
    if char == "K":
        return check_king(position)
    elif char == "Q":
        return check_queen(position)
    elif char == "B":
        return check_bishop(position)
    elif char == "R":
        return check_rook(position)
    elif char == "P":
        return check_pawn(position)
    else:
        return []

def draw_board_with_moves(board, char):
    characters = {char: []}
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == char:
                characters[char].append((i, j))
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            found_char = False
            for char, positions in characters.items():
                if (i, j) in positions:
                    print(char, end=' ')
                    found_char = True
                    break
            if not found_char:
                print('.', end=' ')
        print()

def draw_moves(board,char,pos):
    if pos == (-1,-1):
        print("Can't find pieces")
        return -1
    #Check Char
    if char == "K":
        move_list = check_king(pos)
    elif char == "Q":
        move_list = check_queen(pos)
    elif char == "B":
        move_list = check_bishop(pos)
    elif char == "R":
        move_list = check_rook(pos)
    elif char == "P":
        move_list = check_pawn(pos)
    else:
        return -1
    #Draw
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if (i,j) in move_list:
                print('X', end=' ')
            elif (i,j) == pos:
                print(char, end=' ')
            else:
                print('.', end=' ')
        print("")

def is_checkmate(board, king_position):
    if not is_king_checked(board, king_position):
        print("King is not in check, so it's not checkmate.")
        return False

    # Get all valid moves for the king
    king_moves = get_valid_moves(board, king_position)
    for move in king_moves:
        # Simulate the king making the move
        new_board = simulate_move(board, king_position, move)

        # Check if the king is still in check after the move
        if not is_king_checked(new_board, move):
            # Get all possible moves for the opponent's pieces
            opponents_moves = get_opponents_moves(new_board)

            # Check if any of the opponent's pieces can still attack the king after its move
            if not any(king_position in moves for moves in opponents_moves):
                print("Can king escape: Yes")
                print("King can escape to the following squares:")
                draw_board_with_moves(new_board, "K")  # Draw the board with possible escape moves highlighted
                return False

            # Check if the king can capture the attacking piece
            if board[move[0]][move[1]] != '.':
                print("Can king escape: Yes")
                print("King can capture the attacking piece.")
                return False

    print("Can king escape: No")
    return True

def get_opponents_moves(board):
    opponents_moves = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j].isupper():  # Check if the piece belongs to the opponent
                opponent_pos = (i, j)
                opponent_moves = get_valid_moves(board, opponent_pos)
                opponents_moves.extend(opponent_moves)
    return opponents_moves



def simulate_move(board, from_pos, to_pos):
    # Create a copy of the board to simulate the move
    new_board = [row[:] for row in board]
    new_board[to_pos[0]][to_pos[1]] = new_board[from_pos[0]][from_pos[1]]
    new_board[from_pos[0]][from_pos[1]] = '.'
    return new_board


# Test
if __name__ == "__main__":
    filenames = sys.argv[1:]  # Command line arguments after the script name
    if not filenames:
        print("No filenames provided.")
        sys.exit(1)

    for filename in filenames:
        board_string = read_board_from_file(filename)

        format_board = string_to_board(board_string)
        num_rows, num_cols = count_rows_cols(format_board)
        base = create_base(num_rows, num_cols)

        try:
            characters = find_characters(format_board)
            king_positions = characters.get('K', [])
            if len(king_positions) > 0:
                king_position = king_positions[0]
                if is_checkmate(format_board, king_position):
                    print("Checkmate!")
                else:
                    print("Not checkmate yet.")
            else:
                print(f"King not found in {filename}.")
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")
