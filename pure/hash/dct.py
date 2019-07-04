import pure.hash.phash as phash
import math

class DCTHash(phash.PerceptualHash):
    """
    Defines the set of utilities for taking a discrete cosine
    transform perceptual hash of a grid of RGB pixel values. A 
    DCTHash object should be initialized with a valid grid
    (list of lists) of tuple-formatted data.

    Attributes:
        - (!) See parent class for foundation attributes

    Methods:
        - (!) See parent class for overriden methods
    """

    def __init__(self, variable_grid, reduction_size = 32):
        super().__init__(variable_grid, reduction_size)
        self.gs_flag = False

        # init dct grid params
        self.dct_flag = False
        self.dct_grid = phash.VariableGrid((self.reduction_size, \
            self.reduction_size))

    def compute_hash(self, verbose = False) -> None:
        assert self.hash_flag == False

        # reduce grid
        if verbose: print("Reducing grid...\n")
        self.reduce_grid()

        # convert grid to gs
        if verbose: print("Converting grid to grayscale...\n")
        self.__convert_to_gs()

        # iteratively calculate 2d dct 
        if verbose: print("Calcuating 2D DCT...\n")
        for row in range(self.reduction_size):
            for col in range(self.reduction_size):
                self.dct_grid.load_grid_data((row, col), \
                    self.__calc_2d_dct(row, col))

        # strip high frequency readings
        if verbose: print("Stripping high frequency grid readings...\n")
        assert self.reduction_size >= 8
        mean_val = 0
        high_freq_grid = phash.VariableGrid((8, 8))
        for row in range(8):
            for col in range(8):
                if row == 0 and col == 0: continue
                val = self.dct_grid.read_grid_data((row, col))
                high_freq_grid.load_grid_data((row, col), val)
                mean_val += val

        # calculate mean reading value
        if verbose: print("Calculating mean reading value...\n")
        mean_val = mean_val / ((8 ** 2) - 1)

        # compute bit hash
        if verbose: print("Computing bit hash...\n")
        self.hash_res = self.__compute_bit_hash(mean_val, high_freq_grid)
        self.dct_flag = True

        # publish results
        if verbose:
            print("Publishing results...\n")
            self.publish_results()

    def publish_results(self) -> None:
        assert self.dct_flag == True
        print("DCT hash: {}\n".format(self.__join_list_bits(self.hash_res)))
    
    def __compute_bit_hash(self, mean, high_freq_grid):
        hash_res = []
        
        # iteratively calculate bit
        for row in range(8):
            for col in range(8):
                hash_res.append(1 if high_freq_grid.read_grid_data((row, col)) \
                    > mean else 0)
        return hash_res

    def __convert_to_gs(self) -> None:
        assert self.reduction_flag == True

        # iteratively convert to gs
        for row in range(self.reduction_size):
            for col in range(self.reduction_size):
                pixel = self.reduced_data.read_grid_data((row, col))
                self.reduced_data.load_grid_data((row, col), int(sum(pixel) / 3))
        self.gs_flag = True

    def __calc_2d_dct(self, u, v) -> float:
        m_term = 2.0 / self.reduction_size
        iter_sum = 0

        # calculate sum term iteratively
        assert self.gs_flag == True
        for i in range(self.reduction_size):
            for j in range(self.reduction_size):
                lambda_term = self.__calc_lambda(i)
                lambda_term *= self.__calc_lambda(j)
                lambda_term *= self.__calc_cos(u, i)
                lambda_term *= self.__calc_cos(v, j)
                lambda_term *= self.reduced_data.read_grid_data((i, j))
                iter_sum += lambda_term
        
        # return result
        return m_term * iter_sum

    def __calc_cos(self, left, right) -> float:
        cos_term = (math.pi * left) / (2.0 * self.reduction_size)
        cos_term *= 2 * right + 1
        return math.cos(cos_term)

    def __calc_lambda(self, xi) -> float:
        if xi == 0: return 1.0 / math.sqrt(2.0)
        else: return 1.0
    
    def __join_list_bits(self, hash) -> None:
        return "".join([str(x) for x in hash])