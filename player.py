"""
Entry point to the sudoku solver
"""
import argparse
import os
from board import SudokuBoard

MY_PATH = os.path.abspath(os.path.dirname(__file__))


def main():
    """ Main entry point into the sudoku board solver """
    parser = argparse.ArgumentParser()

    parser.add_argument("--file",
                        action="store",
                        dest="file",
                        default=None,
                        help="Path to game board",
                        required=True)

    parser.add_argument("--outfile",
                        action="store",
                        dest="outfile",
                        default=None,
                        help="Path to game board",
                        required=False)

    args = parser.parse_args()

    gameboard = SudokuBoard(os.path.join(MY_PATH, args.file))
    gameboard.print_board()
    gameboard.print_board(True)

    if args.outfile is not None:
        gameboard.output_board_to_file(args.outfile)


if __name__ == "__main__":
    main()
