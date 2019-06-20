import pure.imaging.graphics as graphics
import pure.imaging.grid as grid

class FeatureSet:
    """
    Defines the collective set of features actively applied to an
    image and the group of utilities for managing these features.

    Attributes:
        - feature_set -> set : 

    Methods:

    """
    
    def __init__(self):
        self.feature_set = set()

    def add_feature(self, feature_addition):

        # verify that populated feature focal region
        assert feature_addition.populated == True

class FeatureAddition:
    """
    Defines the attributes and utilities for isolating a single
    feature focal region in an image. Requires the original pixel
    grid in order to populate its data. 

    Attributes:
        - title -> String : title for image feature
        - id -> String : id for image feature
        - pixel_grid -> PixelGrid : underlying pixel grid structure
            on which feature is mounted
        - grid_dimensions -> tuple : height/width dimensions of 
            underlying pixel grid
        - focal_data -> map : pixel values for each pixel index
            pair in focal region on original image
        - focal_dimensions -> tuple : height/width dimensions of 
            focal region
        - populated -> bool : flag for whether the focal region has 
            been populated yet
    
    Methods: 
        - populate_focal_region(position, size) -> None : loads pixel
            values from underlying pixel grid that sit within the 
            focal region boundaries
    """

    def __init__(self, pixel_grid, title, id):
        self.title = title
        self.id = id
        self.pixel_grid = pixel_grid
        self.grid_dimensions = pixel_grid.get_grid_dimensions()
        self.populated = False

        # focal region data params
        self.focal_data = None
        self.focal_dimensions = None
        self.top_left_boundary = None

    def populate_focal_region(self, position, size) -> None:
        assert self.populated == False

        # get tuple values
        row, col = position
        height, width = size
        grid_height, grid_width = self.grid_dimensions

        # assert even dimension sizes
        assert height % 2 == 0
        assert width % 2 == 0

        # populate focal region data
        self.focal_data = {}
        height_slip_min = max(0, row - int(height / 2))
        width_slip_min = max(0, col - int(width / 2))
        height_slip_max = min(grid_height, row + int(height / 2) + 1)
        width_slip_max = min(grid_width, col + int(width / 2) + 1)
        height_range = height_slip_max - height_slip_min
        width_range = width_slip_max - width_slip_min
        for i in range(height_slip_min, height_slip_max):
            for j in range(width_slip_min, width_slip_max):
                self.focal_data[i, j] = self.pixel_grid.get_grid_pixel(i, j)

        # set focal region params
        self.focal_dimensions = (height_range, width_range)
        self.top_left_boundary = (height_slip_min, width_slip_min)
        self.populated = True        
        

