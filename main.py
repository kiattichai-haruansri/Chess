import sys
from checkmate import checkmate,start


def main():
    filenames = sys.argv[1:]  # Command line arguments after the script name
    default_board  = """\
        R...
        .K..
        ..P.
        ....\
        """
    start(filenames,default_board)

    checkmate(filenames)

if __name__ == "__main__":
    main()