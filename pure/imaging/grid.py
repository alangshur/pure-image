import imghdr
from PIL import Image

class PixelGrid:
    """
    Defines the infrastructure for manually handling an 
    image as a grid of pixels.

    Attributes: 
        - file_name -> str : absolute path for image file
        - file_type -> str : type of image file
        - grid -> PIL Image : PIL object for image
        - loaded -> bool : flag for whether the grid has been
            loaded yet
        - height -> int : image height in number of pixels
        - width -> int : image width in number of pixels

    Methods:
        - load_pixel_grid() -> None : loads pixel grid attribute
            from file name attribute 
        - get_grid_pixel(row, col) -> tuple : fetches RGB-tuple values 
            for pixel at coordinate (row, col)
        - print_pixel_grid() -> None : prints entire pixel grid by 
            iterating over the pixel for each row/col
        - output_image() -> None : prints pixel grid to console
    """

    def __init__(self, file_name):
        
        # fetch correct image type
        try: 
            self.file_type = imghdr.what(file_name)
            if self.file_type == None: raise ValueError
        except FileNotFoundError:
            raise ValueError 

        # load other attributes
        self.file_name = file_name
        self.loaded = False

    def load_pixel_grid(self) -> None:

        # prevent double-loading grid
        assert self.loaded == False
        
        # populate pixel grid attributes from PIL object
        img = Image.open(self.file_name)
        self.grid = img.convert('RGB')
        self.loaded = True

        # set dimension attributes
        self.width, self.height = self.grid.size

    def get_grid_pixel(self, row, col) -> tuple:

        # return RGB tuple
        assert self.loaded == True
        return self.grid.getpixel((col, row))

    def print_pixel_grid(self) -> None:

        # print pixel grid
        assert self.loaded == True
        for row in range(self.height):
            print('\nRow {}:'.format(row))
            for col in range(self.width):
                print('({}, {}) -> {}'.format(row, col, \
                    self.get_grid_pixel(row, col)))

    def output_image(self) -> None:

        # output image
        assert self.loaded == True 
        self.grid.show()