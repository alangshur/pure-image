import pure.imaging.pimage as pimage
import numpy as np
import math, uuid, os, random, itertools
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
import cv2 
import scipy
from scipy.misc import imread
import _pickle as pickle
import matplotlib.pyplot as plt

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
        - execute_feature_extraction_pipeline(graphics, ncentroids) -> list : 
            run parameterized feature extraction tuned for best results with 
            optional graphics and cluster centroids with kmeans for best results
    """

    def __init__(self, pimage, num_features = 30, scale_ceil = 500):

        # store relevant parameters
        self.file_name = pimage.file_name
        self.pimage = pimage
        self.num_features = num_features

        # load image
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

    def execute_feature_extraction_pipeline(self, graphics = False, ncentroids = 50) -> set:

        # extract features
        bulk_features = self.__run_tuned_feature_extraction()

        # run kmeans on extracted features
        centroids = self.__run_feature_xmeans(bulk_features)
        
        # add graphics 
        if graphics:
            self.add_list_features('Bulk Features', bulk_features, size = (10, 10))
            self.add_list_features('Feature Centroids', centroids, \
                color = (255, 0, 0), size = (20, 20))
            
            # print graphics
            self.print_added_features()

        return bulk_features

    def __run_feature_agglomerative_clustering(self, features) -> set:

        # run agglomerative clustering algorithm
        agglo = AgglomerativeClustering(n_clusters = 10).fit(np.array(features))
        return agglo.labels_

    def __run_feature_kmeans(self, features, n_clusters) -> list:

        # run kmeans algorithm
        kmeans = KMeans(n_clusters = n_clusters).fit(np.array(features))
        centroids = kmeans.cluster_centers_.astype(int)
        return centroids.tolist()

    def __run_feature_xmeans(self, features, num_init_centers = 10, max_centers = 30, \
        clust_size_threshold = 1, dist_threshold = 10) -> list:

        # run xmeans algorithm
        initial_centers = kmeans_plusplus_initializer(features, num_init_centers).initialize()
        algo = xmeans(features, initial_centers = initial_centers, kmax = max_centers)
        algo.process()
        centroids, clusters = algo.get_centers(), algo.get_clusters()
 
        # pre-process centroids
        p_centroids = []
        for coord in centroids:
            row, col = coord[0], coord[1]
            p_centroids.append((int(round(row)), int(round(col))))

        # determine close centroids
        comb_indices = set()
        for comb in itertools.combinations(range(len(p_centroids)), 2):
            cen, c_cen = p_centroids[comb[0]], p_centroids[comb[1]]
            dist = math.sqrt((cen[0] - c_cen[0]) ** 2 + (cen[1] - c_cen[1]) ** 2)
            if dist <= dist_threshold: comb_indices.add(frozenset(comb))
        
        # find transitive centroid clusters
        trans_centroids = []
        for comb in comb_indices:
            addedFlag = False
            for i in range(len(trans_centroids)):
                if len(trans_centroids[i].intersection(comb)):
                    trans_centroids[i] = trans_centroids[i].union(comb)
                    addedFlag = True
                    break
            if not addedFlag: trans_centroids.append(frozenset(comb))

        # combine close transitive centroids sets
        c_centroids, added_indices = [], set()
        for combs in trans_centroids:
            n_centroid = [0, 0]
            for c_idx in combs:
                added_indices.add(c_idx)
                n_centroid[0] += centroids[c_idx][0]
                n_centroid[1] += centroids[c_idx][1]
            n_centroid[0] /= len(combs)
            n_centroid[1] /= len(combs)
            c_centroids.append(n_centroid)

        # purge under-sized clusters
        for c_idx in range(len(centroids)):
            if c_idx in added_indices or len(clusters[c_idx]) \
                <= clust_size_threshold: continue
            c_centroids.append(centroids[c_idx])
        return c_centroids

    def __run_tuned_feature_extraction(self) -> list:

        features, _ = FEAlgorithms.get_ORB_keypoint(self.img_gs, vector_size = 250)
        return features

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
        - get_harris_corner -> set : selects corners using harris corner
            detection algorithm with sub-pixel accuracy for refined results
        - get_shi_tomasi_corner -> set : selects corners using shi-tomasi corner 
            detection algorithm
        - get_FAST_keypoint -> set : selects corners using FAST feature extraction algorithm
        - get_SIFT_keypoint -> set : selects corners using SIFT feature extraction algorithm
        - get_SURF_keypoint -> set : selects corners using SURF feature extraction algorithm
        - get_KAZE_keypoint -> set : selects corners using KAZE feature extraction algorithm
        - get_AKAZE_keypoint -> set : selects corners using AKAZE feature extraction algorithm
        - get_BRISK_keypoint -> set : selects corners using BRISK feature extraction algorithm
        - get_BRIEF_keypoint -> set : selects corners using BRIEF feature extraction algorithm
        - get_ORB_keypoint -> (list, list) : selects corners using ORB feature extraction algorithm 
            and returns reduced list of features and feature descriptors
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
    def get_FAST_corner(img_gs, threshold = 50) -> set:

        # find FAST corners
        fast = cv2.FastFeatureDetector_create(threshold)
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
    def get_ORB_keypoint(img_gs, nfeatures = 1000, vector_size = 200) -> (list, list):

        # find ORB keypoints
        alg = cv2.ORB_create(nfeatures = nfeatures)
        o_kps = alg.detect(img_gs)
        kps = sorted(o_kps, key = lambda x: -x.response)[:vector_size]
        kps, dsc = alg.compute(img_gs, kps)
        dsc = dsc.flatten()

        # format keypoint objects
        return FEAlgorithms.__get_keypoint_list_tuples(kps), dsc.tolist()

    @staticmethod
    def __get_keypoint_list_tuples(kps) -> list:
        list_tuples = []
        for kp in kps:
            x, y = kp.pt
            list_tuples.append((int(y), int(x)))
        return list_tuples  

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