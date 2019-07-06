# Pure Image

## Dependencies

- Python Imaging Library (PIL)

## Implementation Steps

- (X) Organize module hierarchy
- (X) Build image reading and pixel grid module
- (X) Build image graphics module with feature highlighting
- (X) Build traditional perceptual hash and comparison module
- (X) Build discrete cosine transfer perceptual hash and comparison module
- Build feature selection module
  - Redundant selection methods (SIFT keypoints, corners, clusters, naive pixel values)
- Build keypoint region comparison module
  - Use traditional perceptual hash
  - Use DCT pereceptual hash
  - Use CNN (and other methods?)
  - Use k-means to cluster all the different results
- Build pure image algorithm for comparing images
  - Select most probably features
  - Run features through deterministic randomization scheme
  - Compare keypoint regions
- Build database module
- Build web client

## Module Hierarchy

--- pure
    +--- imaging
         +--- pimage (pimage.py)
         +--- pixel grid (grid.py)
         +--- graphics (graphics.py)
    +--- hash
         +--- perceptual hash (phash.py)
         +--- average hash (average.py)
         +--- DCT hash (dct.py)
    +--- insight
         +--- feature extraction
         +--- focal comparator
