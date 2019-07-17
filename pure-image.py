import pure.imaging.pimage as pimage
import pure.insight.feature as feature
import time, uuid

import numpy as np
from sklearn.cluster import KMeans

try:
    start_time = time.time()
    
    pure_image = pimage.PImage('./samples/chicago.png', 'horse test image', str(uuid.uuid1()))
    feature_extractor = feature.FeatureExtractor(pure_image)
    feature_extractor.execute_feature_extraction_pipeline(graphics = True)

    end_time = time.time()
    print("\nTotal time: {}".format(end_time - start_time))

except EOFError as e:
    print(f"Error: {e}")

