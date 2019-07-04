import pure.imaging.grid as grid
import pure.imaging.graphics as graphics
import pure.imaging.pimage as pimage
import pure.hash.average as average
import pure.hash.phash as phash
import pure.hash.dct as dct
import time

try:
    start_time = time.time()
    
    pure_image = pimage.PImage('./samples/horse.jpg', 'test pure image', '12345')
    dct_hash = dct.DCTHash(pure_image.get_var_grid())
    dct_hash.compute_hash(verbose = True)

    end_time = time.time()
    print("\nTotal time: {}".format(end_time - start_time))

except EOFError as e:
    print(f"Error: {e}")

