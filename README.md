### Software Requirements/Libraries:
- C++17 
- openCV (opencv4)
- pkg-config (note: you may have to manually set PKG_CONFIG_PATH)
- Homebrew (recommended)

# To Do
- Clean current modules (style guidelines)
  - Split perceptual hash modules
  - Add configuration options for full perceptual hash (faster options)
  - Unify reference-passing guidelines and privacy modifiers
  - Build smarter interfaces and documentation
  - Build organizational graph of all modules and future modules
    - All past and future modules
    - Organization and library dependencies
- Wrap all libraries using CMake for maximum compatibility
- Build graphics module:
  - Consider using library instead of BMP for portability
  - Reverse grid printing (tie graphics module into grid)
  - Graphical feature highlighting
- Build discrete cosine transfer perceptual hash
    - Links:
        - https://users.cs.cf.ac.uk/Dave.Marshall/Multimedia/node231.html
        - http://hackerfactor.com/blog/index.php%3F/archives/432-Looks-Like-It.html
    - Separate full and partial phash modules 
    - Redundancy technologies to maximize effectivness
- Implement pure image algorithm (module)
  - Feature and keypoint extraction
    - SIFT keypoints
    - Naive pixel values
  - Add ML algorithm for comparing 32x32 grids (double feedback)
  - Redundancy technologies to maximize effectivness
- Key point scrambbling algorithm (module)
  - Intelligent scrambbling of keypoint results
  - Use fixed hash values based on region hashes
  - Test results and tweak parameters for best success rates
- Implement database module
- Implement web client

# Files
- hash/
    - ihash.h: Defines top-level hash class
    - phash.h: Defines image-based perceptual hash class and utilities
    - dcthash.h: Defines DCT perceptual hash class and utilities
- bmp.h: Defines class and utilities for converting image files into pixel grid
- grid.h: Defines class and utilities for handling raw pixel grids

# Module Hierarchy
.
+--- Hash
     +--- Image Perceptual Hash
     +--- DCT Perceptual Hash
+--- PImage
     +--- BMP Image
          +--- Pixel Grid
     +--- Graphics
    