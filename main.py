import sys
from checkmate import checkmate,string_to_board

def write_board_to_file(board, filename):
    with open(filename, 'w') as file:
        for row in board:
            formatted_row = ' '.join(cell if cell != '.' else '.' for cell in row).rstrip()
            file.write(formatted_row + '\n')


def main():
    filenames = sys.argv[1:]  # Command line arguments after the script name
    if not filenames:
        print("No filenames provided. Writing default board configuration to 'default_board.chess'.")
        default_board  = """\
            . . . . . . . K
            . . . . . . . . 
            . . . . . B . . 
            . . . . . . . . 
            . . . . . . . . 
            . . . . . . . Q 
            . . . . . . . . 
            . . . . . . . . \
        """
        write_board = string_to_board(default_board)
        write_board_to_file(write_board, 'default_board.chess')
        filenames.append('default_board.chess')

    checkmate(filenames)

if __name__ == "__main__":
    main()