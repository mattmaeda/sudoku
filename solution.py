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

        self.filter_unique_grid_vectors()

        if self.board_needs_cleaning:
            self.solve_board()


    def get_index_value_sets(self, index_value):
        """ Returns list of values for the row, column,
            and grid at the given index
        """
        return [self.board.get_all_row_values(index_value),
                self.board.get_all_column_values(index_value),
                self.board.get_all_grid_values(index_value)]


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


    def filter_unique_grid_vectors(self):
        """ Iterates through grids and finds values
            unique to a grid's row or column
        """
        for i in range(board.MAX_RANGE_VALUES):
            grid_values = self.board.get_all_grid_values(i)
            grid_row_uniques = self.find_unique_grid_row_values(grid_values)
            self.remove_other_grid_row_values(i, grid_row_uniques)


    def find_unique_grid_row_values(self, grid_values):
        """ Finds values within a grid that are unique
            to a particular grid row and returns that
            value, the row index, and the grid number
        """
        row_idx = 0
        col_idx = 0
        value_counts = {
            row_idx: []
        }

        for values in grid_values:
            if col_idx == 3:
                row_idx += 1
                col_idx = 0
                value_counts[row_idx] = []

            col_idx += 1

            if len(values) == 1:
                continue

            for value in values:
                if value not in value_counts[row_idx]:
                    value_counts[row_idx].append(value)

        set1 = set(value_counts[0])
        set2 = set(value_counts[1])
        set3 = set(value_counts[2])

        return {
            0: list(set1 - set2 - set3),
            1: list(set2 - set1 - set3),
            2: list(set3 - set1 - set2)
        }


    def remove_other_grid_row_values(self, exclude_grid_number,
                                     grid_row_uniques):
        """ From a given row, remove value in row coordinate
            not a part of a specified grid
        """
        column_values = self.board.get_column_values_for_grid(exclude_grid_number)

        for row_index, uniques in grid_row_uniques.iteritems():
            row_coordinate = self.board.get_row_coord_by_grid_row_index(exclude_grid_number,
                                                                        row_index)

            if uniques:
                values = self.board.get_all_row_values(row_coordinate)
                #values_copy = copy(values)

                for i in range(board.MAX_RANGE_VALUES):
                    if i in column_values:
                        continue

                    for unique in uniques:
                        if unique in values[i]:
                            values[i].remove(unique)
                            self.board_needs_cleaning = True



    def find_unique_grid_column_values(self):
        """ Finds values within a grid that are unique
            to a particular grid column and returns that
            value, the column index, and the grid number
        """
        pass


    def remove_other_grid_column_values(self, value, row_index,
                                        exclude_grid_number):
        """ From a given column, remove value in row coordinate
            not a part of a specified grid
        """
        pass
