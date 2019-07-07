import pure.imaging.pimage as pimage
import pure.insight.feature as feature
import time
import uuid

try:
    start_time = time.time()
    
    # initialize pure image object
    pure_image = pimage.PImage('./samples/landscape.jpg', 'horse test image', str(uuid.uuid1()))
    feature_extractor = feature.FeatureExtractor(pure_image)

    # run bulk feature extraction
    bulk_features = feature_extractor.run_bulk_feature_extraction([], [], {})
    print(len(bulk_features))

    # # add corner features
    # feature_extractor.add_list_features('harris (corner)', features_harris, color = (255, 0, 0))
    # feature_extractor.add_list_features('shi-tomasi (corner)', features_shi, color = (0, 255, 0))
    # feature_extractor.add_list_features('FAST (corner)', features_fast, color = (255, 255, 255))

    # # add kepyoint features
    # feature_extractor.add_list_features('SIFT (keypoint)', features_sift, color = (0, 0, 255))
    # feature_extractor.add_list_features('SURF (keypoint)', features_surf, color = (255, 255, 0))
    # feature_extractor.add_list_features('KAZE (keypoint)', features_kaze, color = (0, 255, 255))
    # feature_extractor.add_list_features('AKAZE (keypoint)', features_akaze, color = (255, 0, 255))
    # feature_extractor.add_list_features('BRISK (keypoint)', features_brisk, color = (0, 0, 0))
    # feature_extractor.add_list_features('BRIEF (keypoint)', features_brief, color = (255, 192, 203))
    # feature_extractor.add_list_features('ORB (keypoint)', features_orb, color = (255, 165, 0))

    # # print resultsc
    # feature_extractor.print_added_features()

    end_time = time.time()
    print("\nTotal time: {}".format(end_time - start_time))

except EOFError as e:
    print(f"Error: {e}")

