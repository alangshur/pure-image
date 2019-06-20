# Dependencies

- Python Imaging Library (PIL)

# Implementation Steps

- Organize module hierarchy
- Build image reading and pixel grid module
- Build image graphics module with feature highlighting
- Build traditional perceptual hash and comparison module
- Build discrete cosine transfer perceptual hash and comparison module
    - https://users.cs.cf.ac.uk/Dave.Marshall/Multimedia/node231.html
    - http://hackerfactor.com/blog/index.php%3F/archives/432-Looks-Like-It.html
- Build feature selection module
  - Redundant selection methods (SIFT keypoints, corners, clusters, naive pixel values)
- Build feature randomization module with selection probabilities
- Build keypoint region comparison module
  - Use traditional perceptual hash
  - Use DCT pereceptual hash
  - Use CNN (and other methods?)
- Build pure image algorithm for comparing images
  - Select most probably features
  - Run features through deterministic randomization scheme
  - Compare keypoint regions
- Build database module
- Build web client

# Module Hierarchy

--- pure
    +--- imaging
         +--- pimage (pimage.py)
         +--- pixel grid (grid.py)
         +--- graphics (graphics.py)
    +--- hashing
         +--- perceptual hash
         +--- DCT hash
    