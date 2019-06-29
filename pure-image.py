import pure.imaging.grid as grid
import pure.imaging.graphics as graphics
import pure.imaging.pimage as pimage
import time

try:
    start_time = time.time()
    
    # pure_image = pimage.PImage('./samples/spectrum.png', 'test pure image', '12345')
    # pure_image.add_feature('feature 1', '1', (50, 50), color = (255, 0, 0))
    # pure_image.add_feature('feature 2', '2', (100, 100), color = (255, 0, 0), verbose = True)
    # pure_image.output_image()

    

    end_time = time.time()
    print("\nTotal time: {}".format(end_time - start_time))

except Exception as e:
    print(f"Error: {e}")

