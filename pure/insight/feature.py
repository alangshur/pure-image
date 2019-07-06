import pure.imaging.pimage as pimage
import cv2 
import numpy as np
import uuid 

# - Harris corner detector (sub-pixel accuracy)
# - Shi-Tomasi corner detector
# - SIFT keypoint
# - SURF keypoint (faster than SIFT)
# - BRIEF keypoint

class FeatureExtractor:
    """
    Defines a single interface for extracting relevant and
    reproducible features from a pimage object and automating
    the addition of these features to the pimage feature set.

    Attributes:
        - file_name -> str : absolute file path to image
        - pimage -> PImage : pimage object associated with image
            to be processed
        - num_features -> int : the number of features to be removed 
            from the image
        - img -> CV2Image : grayscale CV2Image object loaded through 
            the cv2 imaging library
        - img_gs -> npMatrix : numpy matrix of the 'img' attribute defined
            above

    Methods:
        - print_added_features() -> None : outputs the pimage with the 
            added feature markings
        - add_list_features() -> None : adds the features given by the 
            'features' parameters annotated by the 'group_name' parameter
    """

    def __init__(self, pimage, num_features = 30):

        # store relevant parameters
        self.file_name = pimage.file_name
        self.pimage = pimage
        self.num_features = num_features

        # pre-process image
        self.img = cv2.cvtColor(cv2.imread(self.file_name), cv2.COLOR_BGR2GRAY)
        self.img_gs = np.float32(self.img)

    def print_added_features(self) -> None:
        self.pimage.output_image()

    def add_list_features(self, group_name, features, size = (4, 4), \
        color = (0, 255, 0)) -> None:
        v = 0

        # iteratively add features to pimage
        for feature in features:
            self.pimage.add_feature("{} {}".format(group_name, v), \
                str(uuid.uuid1()), feature, size, color)
            v += 1

class FEAlgorithms:
    """
    Defines a set of static method algorithms that take
    in a numpy matrix of pixel values representing a grayscale
    image and return feature points as a list of row/col tuples. 

    Static Methods:
        - get_harris_corner -> list : selects corners using harris corner
            detection algorithm with sub-pixel accuracy for refined results
    """

    @staticmethod
    def get_harris_corner(img_gs, block_size = 5, ksize = 3, k = 0.04, crit_max_it = 100, \
        crit_epsilon = 0.001, win_size = (5, 5), zero_zone = (-1, -1)) -> list:

        # find harris corners
        dst = cv2.cornerHarris(img_gs, block_size, ksize, k)
        dst = cv2.dilate(dst, None)
        _, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
        dst = np.uint8(dst) 

        # find centroids
        _, _, _, centroids = cv2.connectedComponentsWithStats(dst)

        # define sub-pix refinement criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, \
            crit_max_it, crit_epsilon)
        corners = cv2.cornerSubPix(img_gs, np.float32(centroids), \
            win_size, zero_zone, criteria)
        
        # convert matrix to list tuples
        return FEAlgorithms.__get_matrix_list_tuples(corners)
    
    @staticmethod
    def get_shi_tomasi_corner(img_gs, max_corners = 50, quality_level = 0.01, \
        min_dist = 10) -> list:

        # find shi-tomasi corners
        corners = cv2.goodFeaturesToTrack(img_gs, max_corners, quality_level, \
            min_dist)
        corners = np.int0(corners)

        # convert matrix to list tuples
        return FEAlgorithms.__get_bound_matrix_list_tuples(corners)

    @staticmethod
    def get_FAST_corner(img):

        # find FAST corners
        fast = cv2.FastFeatureDetector_create()
        kps = fast.detect(img, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_list_tuples(kps)

    @staticmethod
    def get_SIFT_keypoint(img, n_features = 400):

        # find shift keypoints
        sift = cv2.xfeatures2d.SIFT_create(n_features)
        kps, _ = sift.detectAndCompute(img, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_list_tuples(kps)

    @staticmethod
    def get_SURF_keypoint(img, n_features = 400):

        # find surf keypoints
        surf = cv2.xfeatures2d.SURF_create(n_features)
        kps, _ = surf.detectAndCompute(img, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_list_tuples(kps)
    
    @staticmethod
    def get_KAZE_keypoint(img):

        # find surf keypoints
        surf = cv2.KAZE_create()
        kps, _ = surf.detectAndCompute(img, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_list_tuples(kps)
    
    @staticmethod
    def get_AKAZE_keypoint(img):

        # find surf keypoints
        surf = cv2.AKAZE_create()
        kps, _ = surf.detectAndCompute(img, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_list_tuples(kps)
    
    @staticmethod
    def get_BRISK_keypoint(img):

        # find surf keypoints
        surf = cv2.BRISK_create()
        kps, _ = surf.detectAndCompute(img, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_list_tuples(kps)

    @staticmethod
    def get_BRIEF_keypoint(img):

        # find BRIEF keypoints
        star = cv2.xfeatures2d.StarDetector_create()
        brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        kps = star.detect(img, None)
        kps, _ = brief.compute(img, kps)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_list_tuples(kps)
    
    @staticmethod
    def get_ORB_keypoint(img):

        # find ORB keypoints
        orb = cv2.ORB_create()
        kps = orb.detect(img, None)
        kps, _ = orb.compute(img, kps)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_list_tuples(kps)

    @staticmethod
    def __get_keypoint_list_tuples(kps) -> list:
        list_tuples = []
        for kp in kps:
            x, y = kp.pt
            list_tuples.append((int(y), int(x)))
        return list_tuples  

    @staticmethod
    def __get_bound_matrix_list_tuples(np_matrix) -> list:
        list_tuples = []
        for i in np_matrix:
            x, y = i.ravel()
            list_tuples.append((y, x))
        return list_tuples

    @staticmethod
    def __get_matrix_list_tuples(np_matrix) -> list:
        list_tuples = []
        shape = np_matrix.shape
        for row in range(shape[0]):
            list_tuples.append((int(np_matrix[row][1]), int(np_matrix[row][0])))
        return list_tuples