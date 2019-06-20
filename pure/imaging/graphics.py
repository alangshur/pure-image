import pure.imaging.grid as grid
from copy import deepcopy
import math

class GraphicsImage:
    """
    Defines the infrastructure for manually painting, printing, and 
    viewing graphic images.

    Attributes: 
        - pixel_grid -> PixelGrid : pixel grid object to be modified 
            with graphics utilities

    Methods:
        - draw_pixel(row, col, red, green, blue) -> None : layer specified
            pixel on top of pixel grid 
        - draw_square(position, size, color) -> None : uses draw_pixel to 
            to layer square patern on top of pixel grid given by position
            (top-left of square), size, and color parameters
        - draw_feature_pinpoint(position, height, width) -> None : draws a 
            marker for image feature based on mean background pixel values
        - draw_feature_pinpoint_color(position, color, height, width) ->
            None : draws a marker for image feature based on a specified color 
        - output_image() -> None : prints pixel grid to console
    """

    def __init__(self, pixel_grid):

        # load graphics image
        assert pixel_grid.loaded == True
        self.pixel_grid = deepcopy(pixel_grid)

    def draw_pixel(self, row, col, red, green, blue) -> None: 

        # assert RGB-value boundaries
        assert red >= 0 and red < 256
        assert green >= 0 and green < 256
        assert blue >= 0 and blue < 256 

        # place pixel on grid
        self.pixel_grid.grid.putpixel((col, row), (red, green, blue))
    
    def draw_square(self, position, size, color) -> None:

        # get tuple values
        row, col = position
        height, width = size
        red, green, blue  = color

        # draw square pixels
        for i in range(row, row + height):
            for j in range(col, col + width):
                self.draw_pixel(i, j, red, green, blue)

    def draw_feature_pinpoint(self, position, height = 30, width = 30) -> None:
        row, col = position
        mean_colors = [c for c in self.pixel_grid.get_grid_pixel(row, col)]
        row = max(0, row - math.floor(height / 2))
        col = max(0, col - math.floor(width / 2))

        # calculate mean color around position
        for i in range(row, row + height):
            for j in range(col, col + width):
                pass
                red, green, blue = self.pixel_grid.get_grid_pixel(i, j)
                mean_colors[0] += red
                mean_colors[1] += green
                mean_colors[2] += blue

        # normalize results
        inverted_colors = tuple(int(255 - (c / ((height * width) + 1))) \
            for c in mean_colors)

        # draw square
        self.draw_square((row, col), (height, width), inverted_colors)
    
    def draw_feature_pinpoint_color(self, position, color, height = 30, width = 30) \
        -> None:

        # draw square
        self.draw_square(position, (height, width), color)

    def output_image(self) -> None:

        # output image
        self.pixel_grid.grid.show()
