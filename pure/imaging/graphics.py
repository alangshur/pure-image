import pure.imaging.grid as grid
from copy import deepcopy
import math

class GraphicsImage:
    """
    Defines the infrastructure for manually painting, printing, and 
    viewing graphic images. A GraphicsImage object is constructed
    using a PixelGrid object (note: modifying the pixel grid attribute
    of the PixelGrid object will not modify the PixelGrid object)

    Attributes: 
        - pixel_grid -> PixelGrid : pixel grid object to be modified 
            with graphics utilities
        - grid_dimensions -> tuple : height/width dimensions for associated
            pixel grid

    Methods:
        - draw_pixel(position, color) -> None : layer specified
            pixel on top of pixel grid 
        - draw_square(position, size, color) -> None : uses draw_pixel to 
            to layer square patern on top of pixel grid given by position
            (top-left of square), size, and color parameters
        - draw_feature_invert(position, size) -> None : draws a 
            marker for image feature based on mean background pixel values
        - draw_feature_color(position, color, size) -> None : draws a marker 
            for image feature based on a specified color 
        - replace_square_data(self, position, size, data) -> replaces values
            in grid using provided data at position for specified size
        - output_image() -> None : prints pixel grid to console
    """

    def __init__(self, pixel_grid):

        # load graphics image
        assert pixel_grid.loaded == True
        self.pixel_grid = deepcopy(pixel_grid)
        self.grid_dimensions = pixel_grid.get_grid_dimensions()

    def draw_pixel(self, position, color) -> None: 

        # get tuple values
        row, col = position
        red, green, blue = color
        grid_height, grid_width = self.grid_dimensions

        # assert RGB-value boundaries
        assert red >= 0 and red < 256
        assert green >= 0 and green < 256
        assert blue >= 0 and blue < 256 

        # assert boundary values
        assert row <= grid_height
        assert col <= grid_width

        # place pixel on grid
        self.pixel_grid.grid.putpixel((col, row), color)
    
    def draw_square(self, position, size, color) -> None:

        # get tuple values
        row, col = position
        height, width = size
        grid_height, grid_width = self.grid_dimensions

        # draw square pixels
        for i in range(row, row + height):
            if i > grid_height: break
            for j in range(col, col + width):
                if j > grid_width: break
                self.draw_pixel((i, j), color)

    def draw_feature_invert(self, position, size = (30, 30)) -> None:
        
        # get dimension values and position color
        row, col = position
        height, width = size
        grid_height, grid_width = self.grid_dimensions
        mean_colors = [c for c in self.pixel_grid.get_grid_pixel(row, col)]
        height_slip_min = max(0, row - int(height / 2))
        width_slip_min = max(0, col - int(width / 2))
        height_slip_max = min(grid_height, row + int(height / 2) + 1)
        width_slip_max = min(grid_width, col + int(width / 2) + 1)

        # calculate mean color around position
        for i in range(height_slip_min, height_slip_max):
            for j in range(width_slip_min, width_slip_max):
                red, green, blue = self.pixel_grid.get_grid_pixel(i, j)
                mean_colors[0] += red
                mean_colors[1] += green
                mean_colors[2] += blue

        # normalize results
        height_range = height_slip_max - height_slip_min
        width_range = width_slip_max - width_slip_min
        inverted_colors = tuple(int(255 - (c / ((height_range * width_range) \
            + 1))) for c in mean_colors)
        
        # draw square
        self.draw_square((height_slip_min, width_slip_min), (height_range, \
            width_range), inverted_colors)
    
    def draw_feature_color(self, position, color, size = (30, 30)) -> None:
        
         # get dimension values and position color
        row, col = position
        height, width = size
        grid_height, grid_width = self.grid_dimensions
        height_slip_min = max(0, row - int(height / 2))
        width_slip_min = max(0, col - int(width / 2))
        height_slip_max = min(grid_height, row + int(height / 2) + 1)
        width_slip_max = min(grid_width, col + int(width / 2) + 1)

        # draw square
        height_range = height_slip_max - height_slip_min
        width_range = width_slip_max - width_slip_min
        self.draw_square((height_slip_min, width_slip_min), (height_range, \
            width_range), color)

    def replace_square_data(self, position, size, data) -> None:

        # get tuple values and assert size parameters
        row, col = position
        height, width = size
        assert len(data) == height * width
        
        # replace data iteratively
        for i in range(row, row + height):
            for j in range(col, col + width):
                self.draw_pixel((i, j), data[i, j])

    def output_image(self) -> None:

        # output image
        self.pixel_grid.grid.show()
