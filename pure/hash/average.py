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
        horizontal_overflow = self.data.width % self.reduction_size

        # compute mean pixel values
        for row in range(self.reduction_size - 1):
            for col in range(self.reduction_size - 1):
                pixel_sum = (0, 0, 0)

                # sum pixels for quadrant
                for p_row in range(row * vertical_offset, (row + 1) * vertical_offset):
                    for p_col in range(col * horizontal_offset, (col + 1) * horizontal_offset):
                        pixel_val = self.data.read_grid_data((p_row, p_col))
                        pixel_sum = tuple(sum(x) for x in zip(pixel_sum, pixel_val))

                # normalize pixel sum
                pixel_res = tuple(x / (vertical_offset * horizontal_offset) for x in pixel_sum)
                self.reduced_data.load_grid_data((row, col), pixel_res) 
                

        self.reduction_flag = True