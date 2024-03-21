import sys
from checkmate import checkmate, start

def main():
    filenames = sys.argv[1:]  # Command line arguments after the script name
    input_string = ""  # Initialize an empty input string
    
    # Start the program, if filenames are provided, they will be processed; otherwise, user input will be requested to create a default board
    start(filenames, input_string)
    
    # Check for checkmate in the provided board configurations
    checkmate(filenames)

if __name__ == "__main__":
    main()
