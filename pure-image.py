import pure.imaging.grid as grid
import pure.imaging.graphics as graphics
import pure.imaging.pimage as pimage
import time

try:
    start_time = time.time()
    pixel_grid = grid.PixelGrid('./samples/chicago-paint.png')
    pixel_grid.load_pixel_grid()
    
    p_image = pimage.FeatureAddition(pixel_grid, "random title", "123")
    p_image.populate_focal_region((500, 500), (50, 50))

    g_image = graphics.GraphicsImage(pixel_grid)
    g_image.draw_feature_invert((500, 500), (50, 50))
    g_image.output_image()

    g_image.replace_square_data(p_image.top_left_boundary, \
        p_image.focal_dimensions, p_image.focal_data)
    g_image.output_image()

    end_time = time.time()
    print("\nTotal time: {}".format(end_time - start_time))

except Exception as e:
    print(f"Error: {e}")

