import pure.imaging.pimage as pimage
import numpy as np
import math, uuid
import cv2 

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
        - img -> NPArray : grayscale CV2Image object loaded through 
            the cv2 imaging library converted to a numpy matrix/array
        - img_gs -> CV2Image : grayscale CV2Image object loaded through 
            the cv2 imaging library
        - img_np -> npMatrix : numpy matrix of the 'img' attribute defined
            above
        - vert_scale -> float : vertical scale change when resizing input
            image in pre-processing
        - horiz_scale -> float : horizontal scale change when resizing input
            image in pre-processing

    Methods:
        - print_added_features() -> None : outputs the pimage with the 
            added feature markings
        - add_list_features() -> None : adds features associated with the
            pre-processed 'img_gs' and 'img_np' given by the 'features' 
            parameters and annotated by the 'group_name' parameter
    """

    def __init__(self, pimage, num_features = 30, scale_ceil = 500):

        # store relevant parameters
        self.file_name = pimage.file_name
        self.pimage = pimage
        self.num_features = num_features

        # pre-process image
        img = cv2.imread(self.file_name)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # re-scale image for processing
        height, width = img.shape
        if width <= scale_ceil and height <= scale_ceil:
            n_width = width
            n_height = height
        elif width > height:
            n_width = scale_ceil
            n_height = math.floor(height * (n_width / width))
        else:
            n_height = scale_ceil
            n_width = math.floor(width * (n_height / height))

        # get scale ratios
        self.vert_scale = height / n_height
        self.horiz_scale = width / n_width

        # pre-process image
        self.img_gs = cv2.resize(img, (n_width, n_height))
        self.img_np = np.float32(self.img_gs)

        # create np feature extractor library
        self.fe_lib_np = { \
            'harris': FEAlgorithms.get_harris_corner, \
            'shi': FEAlgorithms.get_shi_tomasi_corner, \
        }
        
        # create gs feature extractor library
        self.fe_lib_gs = { \
            'fast': FEAlgorithms.get_FAST_corner, \
            'sift': FEAlgorithms.get_SIFT_keypoint, \
            'surf': FEAlgorithms.get_SURF_keypoint, \
            'kaze': FEAlgorithms.get_KAZE_keypoint, \
            'akaze': FEAlgorithms.get_AKAZE_keypoint, \
            'brisk': FEAlgorithms.get_BRISK_keypoint, \
            'brief': FEAlgorithms.get_BRIEF_keypoint, \
            'orb': FEAlgorithms.get_ORB_keypoint \
        }

    def run_bulk_feature_extraction(self, fe_np, fe_gs, no_include, params) -> list:
        bulk_features = set()

        # run all for empty fe_np and fe_gs
        if len(fe_np) == 0: fe_np = ['harris', 'shi']
        if len(fe_gs) == 0: fe_gs = ['fast', 'sift', 'surf', 'kaze', \
            'akaze', 'brisk', 'brief', 'orb']

        # execute np feature extraction
        for fe in fe_np:
            if fe in no_include: continue
            if fe in params: 
                bulk_features = bulk_features.union(self.fe_lib_np[fe](self.img_np, **params[fe]))
            else: bulk_features = bulk_features.union(self.fe_lib_np[fe](self.img_np))
        
        # execute gs feature extraction
        for fe in fe_gs:
            if fe in no_include: continue
            if fe in params: 
                bulk_features = bulk_features.union(self.fe_lib_gs[fe](self.img_gs, **params[fe]))
            else: bulk_features = bulk_features.union(self.fe_lib_gs[fe](self.img_gs))
        return bulk_features
        
    def print_added_features(self) -> None:
        self.pimage.output_image()

    def add_list_features(self, group_name, features, size = (4, 4), \
        color = (0, 255, 0)) -> None:
        v = 0

        # iteratively add features to pimage
        for feature in features:
            height = int(round(float(feature[0]) * self.vert_scale))
            width = int(round(float(feature[1]) * self.horiz_scale))
            self.pimage.add_feature("{} {}".format(group_name, v), \
                str(uuid.uuid1()), (height, width), size, color)
            v += 1

    def __find_lcd(self, a, b, ceil) -> int:
        lcm = (a * b) // self.__find_gcd(a, b)
        return lcm
    
    def __find_gcd(self, a, b) -> int: 
        while(b): a, b = b, a % b 
        return a

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
    def get_harris_corner(img_np, block_size = 5, ksize = 3, k = 0.04, crit_max_it = 100, \
        crit_epsilon = 0.001, win_size = (5, 5), zero_zone = (-1, -1)) -> set:

        # find harris corners
        dst = cv2.cornerHarris(img_np, block_size, ksize, k)
        dst = cv2.dilate(dst, None)
        _, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
        dst = np.uint8(dst) 

        # find centroids
        _, _, _, centroids = cv2.connectedComponentsWithStats(dst)

        # define sub-pix refinement criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, \
            crit_max_it, crit_epsilon)
        corners = cv2.cornerSubPix(img_np, np.float32(centroids), \
            win_size, zero_zone, criteria)
        
        # convert matrix to list tuples
        return FEAlgorithms.__get_matrix_set_tuples(corners)
    
    @staticmethod
    def get_shi_tomasi_corner(img_np, max_corners = 50, quality_level = 0.01, \
        min_dist = 10) -> set:

        # find shi-tomasi corners
        corners = cv2.goodFeaturesToTrack(img_np, max_corners, quality_level, \
            min_dist)
        corners = np.int0(corners)

        # convert matrix to list tuples
        return FEAlgorithms.__get_bound_matrix_set_tuples(corners)

    @staticmethod
    def get_FAST_corner(img_gs) -> set:

        # find FAST corners
        fast = cv2.FastFeatureDetector_create()
        kps = fast.detect(img_gs, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_set_tuples(kps)

    @staticmethod
    def get_SIFT_keypoint(img_gs, n_features = 400) -> set:

        # find shift keypoints
        sift = cv2.xfeatures2d.SIFT_create(n_features)
        kps, _ = sift.detectAndCompute(img_gs, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_set_tuples(kps)

    @staticmethod
    def get_SURF_keypoint(img_gs, n_features = 400) -> set:

        # find surf keypoints
        surf = cv2.xfeatures2d.SURF_create(n_features)
        kps, _ = surf.detectAndCompute(img_gs, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_set_tuples(kps)
    
    @staticmethod
    def get_KAZE_keypoint(img_gs) -> set:

        # find surf keypoints
        surf = cv2.KAZE_create()
        kps, _ = surf.detectAndCompute(img_gs, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_set_tuples(kps)
    
    @staticmethod
    def get_AKAZE_keypoint(img_gs) -> set:

        # find surf keypoints
        surf = cv2.AKAZE_create()
        kps, _ = surf.detectAndCompute(img_gs, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_set_tuples(kps)
    
    @staticmethod
    def get_BRISK_keypoint(img_gs) -> set:

        # find surf keypoints
        surf = cv2.BRISK_create()
        kps, _ = surf.detectAndCompute(img_gs, None)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_set_tuples(kps)

    @staticmethod
    def get_BRIEF_keypoint(img_gs) -> set:

        # find BRIEF keypoints
        star = cv2.xfeatures2d.StarDetector_create()
        brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        kps = star.detect(img_gs, None)
        kps, _ = brief.compute(img_gs, kps)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_set_tuples(kps)
    
    @staticmethod
    def get_ORB_keypoint(img_gs) -> set:

        # find ORB keypoints
        orb = cv2.ORB_create()
        kps = orb.detect(img_gs, None)
        kps, _ = orb.compute(img_gs, kps)

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_set_tuples(kps)

    @staticmethod
    def __get_keypoint_set_tuples(kps) -> set:
        set_tuples = set()
        for kp in kps:
            x, y = kp.pt
            set_tuples.add((int(y), int(x)))
        return set_tuples  

    @staticmethod
    def __get_bound_matrix_set_tuples(np_matrix) -> set:
        set_tuples = set()
        for i in np_matrix:
            x, y = i.ravel()
            set_tuples.add((int(y), int(x)))
        return set_tuples

    @staticmethod
    def __get_matrix_set_tuples(np_matrix) -> set:
        set_tuples = set()
        shape = np_matrix.shape
        for row in range(shape[0]):
            set_tuples.add((int(np_matrix[row][1]), int(np_matrix[row][0])))
        return set_tuples