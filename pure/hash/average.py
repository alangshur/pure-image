import pure.hash.phash as phash
import math

class AverageHash(phash.PerceptualHash):
    """
    Defines the set of utilities for taking a standard
    perceptual hash of a grid of RGB pixel values. A 
    PerceptualHash object should be initialized with a valid grid
    (list of lists) of tuple-formatted data.

    Attributes:
        - (!) See parent class for foundation attributes
        - red_hash -> list : red hash bits reprented as list
        - green_hash -> list : green hash bits reprented as list
        - blue_hash -> list : blue hash bits reprented as list
        - gs_hash -> list : grayscale hash bits reprented as list
        - lum_hash -> list : luminosity hash bits reprented as list

    Methods:
        - (!) See parent class for overriden methods

    """
    
    def __init__(self, variable_grid):
        super().__init__(variable_grid)
    
    def compute_hash(self, verbose = False) -> None:
        assert self.hash_flag == False

        # reduce grid
        if verbose: print("Reducing grid...\n")
        self.reduce_grid()
        
        # compute pixel mean
        if verbose: print("Computing reduced grid mean...\n")
        pixel_mean = self.__compute_mean()

        # calculate bit hashes
        if verbose: print("Computing all bit hashes...\n")
        self.red_hash = self.__compute_bit_hash(pixel_mean[0], 0)
        self.green_hash = self.__compute_bit_hash(pixel_mean[1], 1)
        self.blue_hash = self.__compute_bit_hash(pixel_mean[2], 2)
        self.gs_hash = self.__compute_gs_bit_hash(sum(pixel_mean) / 3, (1, 1, 1))
        self.lum_hash = self.__compute_gs_bit_hash(.2126 * pixel_mean[0] + .7152 * pixel_mean[1] + \
            .0722 * pixel_mean[2], (.2126, .7152, .0722))
        self.hash_flag = True

        # publish results
        if verbose: 
            print("Publishing results...\n")
            self.publish_results()
        
    def __compute_mean(self) -> tuple:
        assert self.reduction_flag == True
        pixel_sum = (0, 0, 0)

        # iteratively compute pixel mean
        for row in range(self.reduction_size):
            for col in range(self.reduction_size):
                pixel_val = self.reduced_data.read_grid_data((row, col))
                pixel_sum = tuple(sum(x) for x in zip(pixel_sum, pixel_val))
        
        # normalize pixel sum
        return tuple(x / (self.reduction_size ** 2) for x in pixel_sum)

    def __compute_bit_hash(self, mean, key):
        hash_res = []
        
        # iteratively calculate bit
        for row in range(self.reduction_size):
            for col in range(self.reduction_size):
                hash_res.append(1 if self.reduced_data.read_grid_data((row, col))[key] \
                    > mean else 0)
        return hash_res
    
    def __compute_gs_bit_hash(self, mean, coef):
        hash_res = []
        
        # iteratively calculate bit
        for row in range(self.reduction_size):
            for col in range(self.reduction_size):
                pixel_val = self.reduced_data.read_grid_data((row, col))
                hash_res.append(1 if (coef[0] * pixel_val[0] + coef[1] * pixel_val[1] + \
                    coef[2] * pixel_val[2]) / (coef[0] + coef[1] + coef[2]) > mean else 0)
        return hash_res
                
    def publish_results(self) -> None:
        assert self.hash_flag == True
        print("Red hash: {}\n".format(self.__join_list_bits(self.red_hash)))
        print("Green hash: {}\n".format(self.__join_list_bits(self.green_hash)))
        print("Blue hash: {}\n".format(self.__join_list_bits(self.blue_hash)))
        print("Grayscale hash: {}\n".format(self.__join_list_bits(self.gs_hash)))
        print("Luminosity hash: {}\n".format(self.__join_list_bits(self.lum_hash)))    

    def __join_list_bits(self, hash) -> None:
        return "".join([str(x) for x in hash])