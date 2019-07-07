import pure.imaging.graphics as graphics
import pure.imaging.grid as grid
import pure.hash.phash as phash

class FeatureAddition:
    """
    Defines the attributes and utilities for isolating a single
    feature focal region in an image. A FeatureAddition object
    requires the original pixel grid in order to populate its data. 

    Attributes:
        - title -> str : title for image feature
        - id -> String : id for image feature
        - pixel_grid -> PixelGrid : underlying pixel grid structure
            on which feature is mounted
        - grid_dimensions -> tuple : height/width dimensions of 
            underlying pixel grid
        - focal_data -> dict : pixel values for each pixel index
            pair in focal region on original image
        - focal_dimensions -> tuple : height/width dimensions of 
            focal region
        - populated -> bool : flag for whether the focal region has 
            been populated yet
        - position -> tuple : center position for feature focal region
             in pixel grid
        - size -> tuple : dimensionality of feature focal region in 
            pixel grid
        - graphics -> bool : flag for whether or not the feature addition
            was drawn on the graphics image
    
    Methods: 
        - populate_focal_region(position, size) -> None : loads pixel
            values from underlying pixel grid that sit within the 
            focal region boundaries
    """

    def __init__(self, pixel_grid, title, id, graphics = True):
        self.title = title
        self.id = id
        self.pixel_grid = pixel_grid
        self.grid_dimensions = pixel_grid.get_grid_dimensions()
        self.populated = False
        self.graphics = graphics

        # focal region data params
        self.focal_data = None
        self.focal_dimensions = None
        self.top_left_boundary = None

    def populate_focal_region(self, position, size) -> None:
        assert self.populated == False

        # store feature data
        self.position = position
        self.size = size

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
        
class FeatureSet:
    """
    Defines the collective set of features actively applied to an
    image and the group of utilities for managing these features.

    Attributes:
        - feature_set -> set : the feature set containing all the 
            current features

    Methods:
        - add_feature(feature_addition) -> None : add a feature 
            to the feature set 
        - remove_feature(feature_id) -> FeatureAddition : remove a 
            feature from the feature set and return the removed 
            feature object
        - print_feature_set() -> None : print a list of the 
            features ("id: title")
    """
    
    def __init__(self):
        self.feature_set = set()

    def add_feature(self, feature_addition) -> None:

        # verify populated feature focal region
        assert feature_addition.populated or not feature_addition.graphics
        assert feature_addition not in self.feature_set
        self.feature_set.add(feature_addition)

    def remove_feature(self, feature_id) -> FeatureAddition:

        # search for feature
        found_feature = None
        for feature in self.feature_set:
            if feature.id == feature_id: 
                found_feature = feature
                break

        # remove feature
        assert found_feature != None 
        self.feature_set.remove(found_feature)
        return found_feature

    def print_feature_set(self) -> None:
        for feature in self.feature_set:
            print("{}: {}".format(feature.id, feature.title))

class PImage:
    """
    Encapsulating imaging class that ties in grapics, pixel grids,
    and features additions/sets. A PImage object is constructed 
    from a valid image file, which is immediately converted to a 
    pixel grid.

    Attributes:
        - file_name -> String : absolute file path for specified  
            image
        - title -> String : pimage title
        - id -> String : pimage id
        - pixel_grid -> PixelGrid : PixelGrid object associated with
            image file given by file_name
        - gimage -> GraphicsImage : graphics image attached to pimage 
            object based on image pixel grid
        - feature_set -> FeatureSet : collection of features associated
            with pimage and drawn onto graphics image
    
    Methods:
        - add_feature(title, id, position, size, color, verbose) ->
            None : adds a feature to the pimage feature set and
            populates the graphics image with new feature parameters
        - remove_feature(id) -> None : removes the feature in the 
            pimage feature set attached to the specified id
        - output_image() -> None : outputs the graphics image attached
            to the pimage
        - get_var_grid() -> VariableGrid : converts the PImage pixel grid
            to a variable grid
    """
    
    def __init__(self, file_name, title, id):
        self.title = title
        self.id = id

        # load pixel grid (first copy)
        self.file_name = file_name
        self.pixel_grid = grid.PixelGrid(file_name)
        self.pixel_grid.load_pixel_grid()

        # add graphics/features data (second copy)
        self.gimage = graphics.GraphicsImage(self.pixel_grid)
        self.feature_set = FeatureSet()

    def add_feature(self, title, id, position, size = (30, 30), \
        color = None, verbose = False, graphics = True):

        # assert image exists and create feature
        feature = FeatureAddition(self.pixel_grid, title, id, graphics = graphics)

        # add feature and draw graphics
        if graphics:
            feature.populate_focal_region(position, size)
            if color != None: 
                self.gimage.draw_feature_color(position, color, size)
            else: self.gimage.draw_feature_invert(position, size)
        self.feature_set.add_feature(feature)
        
        # print success message
        if verbose == True:
            self.feature_set.print_feature_set()

    def remove_feature(self, id, verbose = False):

        # remove feature from feature set and gimage
        feature = self.feature_set.remove_feature(id)
        if feature.graphics:
            self.gimage.replace_square_data(feature.position, feature.size, \
                feature.focal_data)

        # print success message
        if verbose == True:
            self.feature_set.print_feature_set()

    def output_image(self) -> None:
        print("Outputting image...")
        self.gimage.output_image()

    def get_var_grid(self) -> phash.VariableGrid:
        return self.pixel_grid.get_var_grid()