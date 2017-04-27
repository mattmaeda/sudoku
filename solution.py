"""
Encapsulates sudoku game solutions
"""
import board
from copy import copy

class SudokuSolution(object):
    """ Wraps sudoku board class and solves the board
    """
    def __init__(self, sudoku_board):
        self.board = sudoku_board
        self.board_needs_cleaning = False


    def solve_board(self):
        """ Iterates through rows, columns, and
            grids, finds coordinates that are
            already solved, and eliminates the
            same value from the other coordinates
        """
        self.board_needs_cleaning = False

        for i in range(board.MAX_RANGE_VALUES):
            for value_sets in self.get_index_value_sets(i):
                self.prune_duplicate_values(value_sets)
                self.clean_up_naked_pairs(value_sets)

            # Clean out uniques after initial cleaning of board
            for value_sets in self.get_index_value_sets(i):
                self.find_unique_values_in_set(value_sets)

        if self.board_needs_cleaning:
            self.solve_board()


    def get_index_value_sets(self, index_value):
        """ Returns list of values for the row, column,
            and grid at the given index
        """
        return [self.board.get_all_row_values(index_value),
                self.board.get_all_column_values(index_value),
                self.board.get_all_grid_values(index_value)]


    def find_unique_values_in_set(self, set_values):
        """ Finds instances where a single value is unique
            to a specific set.  In that case, other values
            in that coordinate space are eliminated
        """
        value_counts = {}
        for values in set_values:
            if len(values) == 1:
                continue

            for i in values:
                if i in value_counts:
                    value_counts[i] += 1
                else:
                    value_counts[i] = 1

        uniques = [v for v, ct in value_counts.iteritems() if ct == 1]

        for unique in uniques:
            for values in set_values:
                if len(values) == 1:
                    continue
                self.clean_non_unique_from_set(unique, values)


    def clean_non_unique_from_set(self, unique_value, values):
        """ If a unique value exists in a list, all other
            values are removed from that list
        """
        if unique_value in values and len(values) != 1:
            values_copy = copy(values)

            for value in values_copy:
                if value != unique_value:
                    values.remove(value)
                    self.board_needs_cleaning = True


    def prune_duplicate_values(self, set_values):
        """ If set contains a solved value, removes
            that value from other set values
        """
        solved_values = [i[0] for i in set_values if len(i) == 1]

        for solved in solved_values:
            for values in set_values:
                if solved in values and len(values) > 1:
                    values.remove(solved)
                    self.board_needs_cleaning = True


    def clean_up_naked_pairs(self, set_values):
        """ If there are two coordinates within a set
            have the same two remaining values, then
            remove the those two values from every
            other coordinate
        """
        for naked_pair in self.find_naked_pairs(set_values):
            self.remove_naked_pairs(naked_pair, set_values)


    def find_naked_pairs(self, set_values):
        """ Naked pairs occur when there are two values
            within a set that are equal and contain
            the exact same two values
        """
        pairs = [x for x in set_values if len(x) == 2]

        all_pairs = []
        naked_pairs = []

        for pair in pairs:
            if pair in all_pairs:
                naked_pairs.append(pair)
            else:
                all_pairs.append(pair)

        return naked_pairs


    def remove_naked_pairs(self, pair, set_values):
        """ Finds other coordinates that contain one
            or both of the pair values and removes them
        """
        for values in set_values:
            if len(values) == 1 or pair == values:
                continue

            for i in pair:
                if i in values:
                    values.remove(i)
                    self.board_needs_cleaning = True
