from abc import ABCMeta, abstractclassmethod

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
        self.grid = [[0] * self.width ] * self.height

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

    Abstract Methods:
        - compute_hash(varbose) -> dict : abstract method for computing 
            the intended hash and returning a dictionary of the results
        - publish_results() -> None : abstract method for printing the
            results of the hash computed above
    """

    __metaclass__ = ABCMeta

    @abstractclassmethod
    def __init__(self, variable_grid, reduction_size = 8):
        raise NotImplementedError
    
    @abstractclassmethod
    def compute_hash(self, verbose = True) -> dict:
        raise NotImplementedError

    @abstractclassmethod
    def publish_results(self) -> None:
        raise NotImplementedError

"""
Utility function for converting a PixelGrid object
to a VariableGrid object for portability between modules.
"""
def convert_pixel_to_var(pixel_grid) -> VariableGrid:
    assert pixel_grid.loaded == True
    var_grid = VariableGrid(pixel_grid.size)
    height, width = pixel_grid.size

    # iteratively copy and paste pixel data
    for row in range(height):
        for col in range(width):
            pixel = pixel_grid.get_grid_pixel(row, col)
            var_grid.load_grid_data((row, col), pixel)
    
    return var_grid