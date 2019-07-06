import pure.imaging.pimage as pimage
import pure.insight.feature as feature
import time
import uuid

try:
    start_time = time.time()
    
    # initialize pure image object
    pure_image = pimage.PImage('./samples/spectrum.png', 'horse test image', str(uuid.uuid1()))
    feature_extractor = feature.FeatureExtractor(pure_image)

    # run all point detection algorithms
    features_harris = feature.FEAlgorithms.get_harris_corner(feature_extractor.img_gs)
    features_shi = feature.FEAlgorithms.get_shi_tomasi_corner(feature_extractor.img_gs)
    features_fast = feature.FEAlgorithms.get_FAST_corner(feature_extractor.img)
    features_sift = feature.FEAlgorithms.get_SIFT_keypoint(feature_extractor.img)
    features_surf = feature.FEAlgorithms.get_SURF_keypoint(feature_extractor.img)
    features_kaze = feature.FEAlgorithms.get_KAZE_keypoint(feature_extractor.img)
    features_akaze = feature.FEAlgorithms.get_AKAZE_keypoint(feature_extractor.img)
    features_brisk = feature.FEAlgorithms.get_BRISK_keypoint(feature_extractor.img)
    features_brief = feature.FEAlgorithms.get_BRIEF_keypoint(feature_extractor.img)
    features_orb = feature.FEAlgorithms.get_ORB_keypoint(feature_extractor.img)

    # add corner features
    feature_extractor.add_list_features('harris (corner)', features_harris, color = (255, 0, 0))
    feature_extractor.add_list_features('shi-tomasi (corner)', features_shi, color = (0, 255, 0))
    feature_extractor.add_list_features('FAST (corner)', features_fast, color = (255, 255, 255))

    # add kepyoint features
    feature_extractor.add_list_features('SIFT (keypoint)', features_sift, color = (0, 0, 255))
    feature_extractor.add_list_features('SURF (keypoint)', features_surf, color = (255, 255, 0))
    feature_extractor.add_list_features('KAZE (keypoint)', features_kaze, color = (0, 255, 255))
    feature_extractor.add_list_features('AKAZE (keypoint)', features_akaze, color = (255, 0, 255))
    feature_extractor.add_list_features('BRISK (keypoint)', features_brisk, color = (0, 0, 0))
    feature_extractor.add_list_features('BRIEF (keypoint)', features_brief, color = (255, 192, 203))
    feature_extractor.add_list_features('ORB (keypoint)', features_orb, color = (255, 165, 0))

    # print results
    feature_extractor.print_added_features()

    end_time = time.time()
    print("\nTotal time: {}".format(end_time - start_time))

except EOFError as e:
    print(f"Error: {e}")

