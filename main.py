import sys
from checkmate import checkmate,start


def main():
    filenames = sys.argv[1:]  # Command line arguments after the script name
    input_string =""
    
    start(filenames,input_string)

    

    checkmate(filenames)

if __name__ == "__main__":
    main()