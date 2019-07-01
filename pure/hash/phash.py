from abc import ABCMeta, abstractclassmethod
import math

class VariableGrid:
    """
    Defines an encapsulation system for variable-sized 
    grids of pixel data. A VariableGrid object is instanitated
    using the intended dimensions of the container and then
    loaded using manual function calls. 

    Attributes:
        - self.height -> int : grid height (number of rows)
        - self.width -> int : grid width (number of columns)
        - self.grid -> list(list) : grid of pixel values represented
            as list of list of tuples

    Methods:
        - load_grid_data(location, data) -> None : load grid data
            for a single specified location and pixel value
        - read_grid_data(location) -> tuple : fetch grid data for
            a single specified location in the grid
        - print_grid_data() -> None : output entire formatted grid
    """

    def __init__(self, size):
        self.height, self.width = size
        self.grid = [[0] * self.width for _ in range(self.height)]

    def load_grid_data(self, location, data) -> None:
        row, col = location

        # validate input data
        assert row < self.height
        assert col < self.width
        assert isinstance(data, tuple)
        assert len(data) == 3

        # load data
        self.grid[row][col] = data

    def read_grid_data(self, location) -> tuple:
        row, col = location 

        # validate input data
        assert row < self.height
        assert col < self.width

        # fetch data
        return self.grid[row][col]

    def print_grid_data(self) -> None:
        for row in range(self.height):
            print('\nRow {}:'.format(row))
            for col in range(self.width):
                print('({}, {}) -> {}'.format(row, col, \
                    self.read_grid_data((row, col))))
        
class PerceptualHash:
    """
    Defines an abstract parent class for average and DCT hash classes.
    All perceptual hash classes are instanitated using a variable grid
    defined by the VariableGrid class above.

    Attributes:
        - data -> VariableGrid : variable grid representation of the
            grid to be hashed
        - hash_flag -> bool : stamp attribute for checking whether the 
            main 'compute_hash' method has been executed
        - reduction_size -> int : square dimension parameters for grid
            reduction method
        - reduction_flag -> bool : stamp attribute for checking whether
            the reduction method '__reduce_grid' hash been executed
        - reduced_data -> VariableGrid : reduced variable grid object 
            after executing reduction method '__reduce_grid'

    Abstract Methods:
        - compute_hash(varbose) -> dict : abstract method for computing 
            the intended hash and returning a dictionary of the results
        - publish_results() -> None : abstract method for printing the
            results of the hash computed above
        - redice_grid() -> None : utility method intended for subclasses
            to reduce variable grid into a averaged square variable grid
            of dimensiomn 'reduction_size' by 'reduction_size'
    """

    __metaclass__ = ABCMeta

    def __init__(self, variable_grid, reduction_size = 8):
        self.data = variable_grid

        # init hash data
        self.hash_flag = False

        # init reduction data
        self.reduction_size = reduction_size
        self.reduction_flag = False
        self.reduced_data = None
    
    @abstractclassmethod
    def compute_hash(self, verbose = False) -> dict:
        raise NotImplementedError

    @abstractclassmethod
    def publish_results(self) -> None:
        raise NotImplementedError

    def reduce_grid(self) -> None:
        assert self.reduction_flag == False
        self.reduced_data = VariableGrid((self.reduction_size, self.reduction_size))

        # assert minimum size constraints
        assert self.data.height >= self.reduction_size
        assert self.data.width >= self.reduction_size

        # get vertical offset conversion sizes
        if self.data.height % self.reduction_size == 0:
            vertical_offset = math.floor(self.data.height / self.reduction_size)
            vertical_compensation = self.reduction_size
        else:
            vertical_offset = math.floor(self.data.height / (self.reduction_size - 1))
            vertical_overflow = self.data.height % (self.reduction_size - 1)
            vertical_compensation = self.reduction_size - 1

        # get horizontal offset conversion sizes
        if self.data.width % self.reduction_size == 0:
            horizontal_offset = math.floor(self.data.width / self.reduction_size)
            horizontal_compensation = self.reduction_size
        else:
            horizontal_offset = math.floor(self.data.width / (self.reduction_size - 1))
            horizontal_overflow = self.data.width % (self.reduction_size - 1)
            horizontal_compensation = self.reduction_size - 1

        # compute mean pixel values
        for row in range(vertical_compensation):
            for col in range(horizontal_compensation):
                pixel_sum = (0, 0, 0)

                # sum pixels for quadrant
                for p_row in range(row * vertical_offset, (row + 1) * vertical_offset):
                    for p_col in range(col * horizontal_offset, (col + 1) * horizontal_offset):
                        pixel_val = self.data.read_grid_data((p_row, p_col))
                        pixel_sum = tuple(sum(x) for x in zip(pixel_sum, pixel_val))

                # normalize pixel sum
                pixel_res = tuple(x / (vertical_offset * horizontal_offset) for x in pixel_sum)
                self.reduced_data.load_grid_data((row, col), pixel_res) 

        # compute vertical offset pixel values
        if vertical_compensation < self.reduction_size:
            for col in range(horizontal_compensation):
                pixel_sum = (0, 0, 0)

                # sum pixels for quadrant
                for p_row in range((self.reduction_size - 1) * vertical_offset, self.data.height):
                    for p_col in range(col * horizontal_offset, (col + 1) * horizontal_offset):
                        pixel_val = self.data.read_grid_data((p_row, p_col))
                        pixel_sum = tuple(sum(x) for x in zip(pixel_sum, pixel_val))

                # normalize pixel sum
                pixel_res = tuple(x / (horizontal_offset * vertical_overflow) for x in pixel_sum)
                self.reduced_data.load_grid_data((self.reduction_size - 1, col), pixel_res)

        # compute horizontal offset pixel values
        if horizontal_compensation < self.reduction_size:
            for row in range(vertical_compensation):
                pixel_sum = (0, 0, 0)

                # sum pixels for quadrant
                for p_row in range(row * vertical_offset, (row + 1) * vertical_offset):
                    for p_col in range((self.reduction_size - 1) * horizontal_offset, self.data.width):
                        pixel_val = self.data.read_grid_data((p_row, p_col))
                        pixel_sum = tuple(sum(x) for x in zip(pixel_sum, pixel_val))

                # normalize pixel sum
                pixel_res = tuple(x / (vertical_offset * horizontal_overflow) for x in pixel_sum)
                self.reduced_data.load_grid_data((row, self.reduction_size - 1), pixel_res)
            
        # compute corner offset pixel value
        if vertical_compensation < self.reduction_size and horizontal_compensation < self.reduction_size:
            pixel_sum = (0, 0, 0)
            for p_row in range((self.reduction_size - 1) * vertical_offset, self.data.height):
                for p_col in range((self.reduction_size - 1) * horizontal_offset, self.data.width):
                    pixel_val = self.data.read_grid_data((p_row, p_col))
                    pixel_sum = tuple(sum(x) for x in zip(pixel_sum, pixel_val))
            pixel_res = tuple(x / (horizontal_overflow * vertical_overflow) for x in pixel_sum)
            self.reduced_data.load_grid_data((self.reduction_size - 1, self.reduction_size - 1), pixel_res)

        # stamp reduction process
        self.reduction_flag = True

"""
Utility function for converting a PixelGrid object
to a VariableGrid object for portability between modules.
"""
def convert_pixel_to_var(pixel_grid) -> VariableGrid:
    assert pixel_grid.loaded == True
    var_grid = VariableGrid(pixel_grid.get_grid_dimensions())
    height, width = pixel_grid.get_grid_dimensions()

    # iteratively copy and paste pixel data
    for row in range(height):
        for col in range(width):
            pixel = pixel_grid.get_grid_pixel(row, col)
            var_grid.load_grid_data((row, col), pixel)
    return var_grid