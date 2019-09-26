# TerrainGenerator
 A web application to generate terrain  
 [terrainRaw.py](./terrainRaw.py) and [terrainRaw2.py](./terrainRaw2.py) is compiled using [makeX5](https://github.com/ILikePython256/makeX/blob/master/makeX5.py).
## Arguments
+ terrain.py:
   Randomizes and expands a flat 1x1 terrain.
   - reps (2): How many times to expand, smoothen and randomize.
+ terrain2.py:
   Generates a randomized seed landscape and randomizes that.
   - reps (2): See above.
   - seed (?): Seed for random landscape.
   - w (2): Width of seed landscape.
   - h (2): Height of seed landscape.
   - flux (0.1): Amount of randomization.
   - range (4.0): Limits of seed landscape.
   Note: Seed is displayed at bottom of page.
