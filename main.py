import sys
from checkmate import checkmate

def main():
    filenames = sys.argv[1:]  # Command line arguments after the script name
    if not filenames:
        print("No filenames provided.")
        sys.exit(1)

    checkmate(filenames)

if __name__ == "__main__":
    main()
