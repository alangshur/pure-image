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
    """

    def __init__(self, size):
        self.height, self.width = size
        self.grid = [[] * self.width ] * self.height

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
        
class PerceptulHash:
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

    

