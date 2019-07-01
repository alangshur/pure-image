import pure.imaging.grid as grid
import pure.imaging.graphics as graphics
import pure.imaging.pimage as pimage
import pure.hash.average as average
import pure.hash.phash as phash
import time

try:
    start_time = time.time()
    
    pure_image = pimage.PImage('./samples/chicago-paint.png', 'test pure image', '12345')
    average_hash = average.AverageHash(pure_image.get_var_grid())
    average_hash.compute_hash(verbose = True)

    end_time = time.time()
    print("\nTotal time: {}".format(end_time - start_time))

except Exception as e:
    print(f"Error: {e}")

