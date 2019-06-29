import pure.hash.phash as phash
import math

class AverageHash(phash.PerceptualHash):
    """
    Defines the set of utilities for taking a standard
    perceptual hash of a grid of RGB pixel values. A 
    PerceptualHash object should be initialized with a valid grid
    (list of lists) of tuple-formatted data.

    Attributes:

    Methods:

    """
    
    def __init__(self, variable_grid, reduction_size = 8):
        self.data = variable_grid
        self.reduction_size = reduction_size
        self.reduction_flag = False
        self.reduced_data = None
    
    def compute_hash(self, verbose = True) -> dict:
        pass

    def publish_results(self) -> None:
        pass

    def __reduce_grid(self) -> None:
        assert self.reduction_flag == False
        self.reduced_data = phash.VariableGrid((self.reduction_size, self.reduction_size))

        # assert minimum size constraints
        assert self.data.height >= self.reduction_size
        assert self.data.width >= self.reduction_size

        # get offset conversion sizes
        vertical_offset = math.floor(self.data.height / self.reduction_size)
        horizontal_offset = math.floor(self.data.width / self.reduction_size)
        vertical_overflow = self.data.height % self.reduction_size


        self.reduction_flag = True