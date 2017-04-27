"""
Contains the Sudoku game board object
"""
from copy import copy

MAX_BOARD_VALUES = 81
MAX_RANGE_VALUES = 9
POSSIBLE_COORDINATE_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]
MAX_TOTAL = 45
TABLE_WIDTH_NORMAL_DISPLAY = 21
TABLE_WIDTH_EXTENDED_DISPLAY = 93

# Set format <grid_value>: [[rows],[cols]]
GRIDS = {
    0: [[0, 1, 2], [0, 1, 2]],
    1: [[0, 1, 2], [3, 4, 5]],
    2: [[0, 1, 2], [6, 7, 8]],
    3: [[3, 4, 5], [0, 1, 2]],
    4: [[3, 4, 5], [3, 4, 5]],
    5: [[3, 4, 5], [6, 7, 8]],
    6: [[6, 7, 8], [0, 1, 2]],
    7: [[6, 7, 8], [3, 4, 5]],
    8: [[6, 7, 8], [6, 7, 8]]
}

class SudokuBoard(object):
    """ Sudoku board object """
    def __init__(self, path_to_board):
        self.board = []
        self.initialize_game_board()

        board_values = self.get_game_board_presets(path_to_board)
        self.preset_board_values(board_values)


    def initialize_game_board(self):
        """ Sets up the blank game board, attaching all possible
            coordinate values at each coordinate
        """
        for row_index in range(MAX_RANGE_VALUES):
            row = []

            for column_index in range(MAX_RANGE_VALUES):
                row.append(copy(POSSIBLE_COORDINATE_VALUES))

            self.board.append(row)


    def get_game_board_presets(self, path_to_board):
        """ Loads the game board presets from file """
        board_values = None

        with open(path_to_board, "r") as handle:
            board_values = handle.read().strip()

            if len(board_values) != MAX_BOARD_VALUES:
                raise Exception("Malformed sudoku game board.")

        return board_values


    def preset_board_values(self, board_values):
        """ Takes the preset board values and sets up the game
            board
        """
        row_coordinate = 0
        column_coordinate = 0

        for coordinate_value in board_values:
            # Increment row every ninth value
            if column_coordinate == MAX_RANGE_VALUES:
                row_coordinate += 1
                column_coordinate = 0

            if coordinate_value != ".":
                self.set_board_value_at_coordinate(row_coordinate,
                                                   column_coordinate,
                                                   int(coordinate_value))

            column_coordinate += 1


    def set_board_value_at_coordinate(self, row_coordinate,
                                      column_coordinate, value):
        """ Sets value at given a row and column coordinate """
        self.board[row_coordinate][column_coordinate] = [value]


    def get_board_value_at_coordinate(self, row_coordinate,
                                      column_coordinate,):
        """ Gets value at a given coordinate """
        return self.board[row_coordinate][column_coordinate]


    def get_all_row_values(self, row_coordinate):
        """ Returns all the values for a given row """
        return self.board[row_coordinate]


    def get_all_column_values(self, column_coordinate):
        """ Returns all the values for a given coordinate """
        return [self.board[row_coordinate][column_coordinate]
                for row_coordinate in range(MAX_RANGE_VALUES)]


    def get_all_grid_values(self, grid_number):
        """ Returns all the values for the given 3 x 3 grid

        Grid numbering as follows:

        # # # | # # # | # # #
        # 0 # | # 1 # | # 2 #
        # # # | # # # | # # #
        ---------------------
        # # # | # # # | # # #
        # 3 # | # 4 # | # 5 #
        # # # | # # # | # # #
        ---------------------
        # # # | # # # | # # #
        # 6 # | # 7 # | # 8 #
        # # # | # # # | # # #

        """
        values = []

        subgrid_coordinates = GRIDS[grid_number]
        for row_coordinate in subgrid_coordinates[0]:
            for column_coordinate in subgrid_coordinates[1]:
                values.append(self.board[row_coordinate][column_coordinate])

        return values


    def validate_board(self):
        """ Validates if the board is correctly solved """
        res = []

        for i in range(MAX_RANGE_VALUES):
            res.append(self.validate_row(i))
            res.append(self.validate_column(i))
            res.append(self.validate_sub_grid(i))

        return False not in res


    def validate_row(self, row_coord):
        """ Validates if row settings are correct """
        return self.check_valid(self.get_all_row_values(row_coord))


    def validate_column(self, col_coord):
        """ Validates if column settings are correct """
        return self.check_valid(self.get_all_column_values(col_coord))


    def validate_sub_grid(self, grid_value):
        """ Validates if sub grid settings are correct """
        return self.check_valid(self.get_all_grid_values(grid_value))


    def check_valid(self, set_values):
        """ Sums the values of a given set are correct """
        return sum(sum(i) for i in set_values) == MAX_TOTAL


    def print_board(self, print_extended_format=False):
        """ Outputs the board state """
        print "\n\n"

        table_width = TABLE_WIDTH_NORMAL_DISPLAY

        if print_extended_format:
            table_width = TABLE_WIDTH_EXTENDED_DISPLAY

        idx = 0

        for row in self.board:

            if idx == 3:
                print "\t{}".format("-" * table_width)
                idx = 0

            fmt_out = self.get_row_outputs(row, print_extended_format)
            print "\t%s %s %s | %s %s %s | %s %s %s" % tuple(fmt_out)

            idx += 1

        print "\n\n"


    def get_row_outputs(self, row_values, use_extended_format):
        """ Gets the formatted output for a given set of row values """
        row_outputs = []
        for values in row_values:
            raw_value = "{}".format("".join(str(i) for i in values))

            if use_extended_format:
                row_outputs.append(raw_value.center(9))
            else:
                if len(raw_value) > 1:
                    row_outputs.append(" ")
                else:
                    row_outputs.append(raw_value)

        return row_outputs

