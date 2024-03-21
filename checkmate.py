from check_move import *

# Manage Board
def string_to_board(multi_line_string):
    # Split the input string into lines
    lines = multi_line_string.strip().split('\n')
    
    # Initialize an empty board
    board = []
    
    # Iterate over each line in the input
    for line in lines:
        # Split the line into individual characters
        row = line.split()
        
        # Check if the row length exceeds the maximum allowed (8)
        if len(row) > 8:
            print("Error: The board is too large.")
            return -1  # Return error code
            
        # Append the row to the board
        board.append(row)
    
    # Check if the board dimensions are consistent
    row_lengths = [len(line.split()) for line in lines]
    if len(set(row_lengths)) != 1:
        print("Error: Unequal row lengths")
        return -1  # Return error code
    
    # Check if the board is square
    if check_board_dimensions_error(board):
        print("Error: Isn't Square")
        return -1  # Return error code

    return board

def create_base(num_rows, num_cols):
    # Create a base board with specified dimensions filled with empty cells
    return [['.' for _ in range(num_cols)] for _ in range(num_rows)]

# Check
def check_board_dimensions_error(board):
    # Check if the board dimensions are consistent
    num_rows = len(board)
    num_cols = len(board[0]) if board else 0

    for row in board:
        if len(row) != num_cols:
            return True  # Dimensions are inconsistent

    if num_rows != num_cols:
        return True  # Dimensions are inconsistent

    return False

# Calculate
def count_rows_cols(board):
    # Calculate the number of rows and columns in the board
    num_rows = len(board)
    if num_rows == 0:
        return 0, 0  # Empty board
    
    num_cols = len(board[0])
    return num_rows, num_cols

def find_characters(board):
    # Find positions of all characters on the board
    characters = {}
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col not in characters:
                characters[col] = []
            characters[col].append((i, j))
    return characters

def is_king_checked(board, king_position):
    # Check if the king is under attack
    characters = find_characters(board)
    attacking_pieces = []
    for char, positions in characters.items():
        if char != 'K':
            for pos in positions:
                if king_position in get_valid_moves(board, pos):
                    attacking_pieces.append((char, pos))
    if attacking_pieces:
        # King is under attack
        print("\nSuccess")
        name = {
            'K': 'King',
            'Q': 'Queen',
            'P': 'Pawn',
            'B': 'Bishop',
            'R': 'Rook',
            'k': 'Knight'
        }
        for char, pos in attacking_pieces:
            print(f"\n{name[char]} ({char}):")
            draw_moves(base, char, pos)
        return True
    else:
        # King is not under attack
        print("\nFail")
        return False

def get_valid_moves(board, position):
    # Get valid moves for a piece at a given position
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
    elif char == "k":
        return check_knight(position)
    else:
        return []

def draw_board_with_moves(board, char):
    # Draw the board with moves for a specific piece highlighted
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

def draw_moves(board, char, pos):
    # Draw possible moves for a piece
    if pos == (-1, -1):
        print("Can't find pieces")
        return -1
    # Check Char
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
    elif char == "k":
        move_list = check_knight(pos)
    else:
                return -1

    # Draw the board with possible moves highlighted
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if (i, j) in move_list:
                print('X', end=' ')
            elif (i, j) == pos:
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
    # Get all possible moves for the opponent's pieces
    opponents_moves = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j].isupper():  # Check if the piece belongs to the opponent
                opponent_pos = (i, j)
                opponent_moves = get_valid_moves(board, opponent_pos)
                opponents_moves.extend(opponent_moves)
    return opponents_moves

def simulate_move(board, from_pos, to_pos):
    # Simulate a move on the board
    print("\nSimulate Move")
    # Create a copy of the board to simulate the move
    try:
        new_board = [row[:] for row in board]
        new_board[to_pos[0]][to_pos[1]] = new_board[from_pos[0]][from_pos[1]]
        new_board[from_pos[0]][from_pos[1]] = '.'
    except Exception as e:
        print(f"Simulate Error: {e} :But I'm Lazy to fix GoodBye")

    return new_board

# Main control
def read_board_from_file(filename):
    # Read the board configuration from a file
    with open(filename, 'r') as file:
        board_string = file.read()
    return board_string

def check_and_fix_string(input_string):
    # Check and fix the input string format
    lines = input_string.strip().split('\n')

    all_chars_have_space = True
    formatted_lines = []
    for line in lines:
        formatted_line = ' '.join(char for char in line)
        formatted_lines.append(formatted_line)
        
        if any(char != ' ' for char in line):
            all_chars_have_space = False

    fixed_string = '\n'.join(formatted_lines)

    if all_chars_have_space:
        pass
    else:
        print("Add space between characters. Fixing...")

    return fixed_string

def write_board_to_file(board, filename): 
    # Write the board configuration to a file
    with open(filename, 'w') as file:
        for row in board:
            formatted_row = ' '.join(cell if cell != '.' else '.' for cell in row).rstrip()
            file.write(formatted_row + '\n')

def start(filenames, default_board): # Fix and write file
    if not filenames:
        print("Enter the board configuration. Input will stop once the number of rows becomes equal to the number of columns:")
        default_board = ""
        while True:
            line = input()
            default_board += line + "\n"
            num_rows = len(default_board.strip().split('\n'))
            num_cols = len(default_board.strip().split('\n')[0].strip())
            if num_rows == num_cols:
                break
        print("No filenames provided. Writing default board configuration to 'default_board.chess'.")
        default_board = check_and_fix_string(default_board)
        write_board = string_to_board(default_board)
        print(write_board)
        write_board_to_file(write_board, 'default_board.chess')
        filenames.append('default_board.chess')

# Run
def checkmate(filenames): # Main function
    for filename in filenames:
        board_string = read_board_from_file(filename)

        format_board = string_to_board(board_string)
        num_rows, num_cols = count_rows_cols(format_board)
        global base 
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
            print(f"An error occurred while processing {filename}: {e} :But I'm Lazy to fix GoodBye")

