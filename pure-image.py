import pure.imaging.grid as grid
import pure.imaging.graphics as graphics
import time

try:
    start_time = time.time()
    pixel_grid = grid.PixelGrid('./samples/chicago-paint.png')
    pixel_grid.load_pixel_grid()

    g_image = graphics.GraphicsImage(pixel_grid)
    g_image.draw_feature_pinpoint((2000, 300), 50, 50)
    g_image.draw_feature_pinpoint_color((500, 500), (0, 0, 255), 50, 50)
    g_image.output_image()

    end_time = time.time()
    print("\nTotal time: {}".format(end_time - start_time))
except Exception as e:
    print(f"Error: {e}")

