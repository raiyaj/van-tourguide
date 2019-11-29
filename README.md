# Setup

## Required libraries
```
pandas
numpy
matplotlib
sklearn
```

## Running code

All scripts in the `src/` directory should be run from the project's root directory, and scripts with a number in the filename should be executed in that order.


<br>**1-just-downtown-vancouver.py**

Args: `input-path`, `output-directory` \
Returns: JSON file containing only points that are roughly within Downtown Vancouver
```
$ python3 src/1-just-downtown-vancouver.py input/vancouver.json input/
```


<br>**2-interesting-heuristic.py**

Args: `input-path`, `output-directory` \
Returns: JSON file containing the same points, but with an added `interesting_heuristic` column (normalized to [0,1])
```
$ python3 src/2-interesting-heuristic.py input/downtown-vancouver.json output/
```
<br>**3-distance.py**

Args: `input-path`, `image-path`,`output-directory` \
Returns: Estimated walking distance, estimated walking time, and veeery rough path to destination
```
$ python3 3-distance.py ../output/downtown-vancouver-heuristic.json ../input/downtown-vancouver.png ../output/
```
<br>**4-interesting-locations.py**

Args: `input-path`, `image-path`,`output-directory` \
Returns: A map with departure location, destination location, and some iteresting locations around the path 

```
$ python3 4-interesting-locations.py ../output/downtown-vancouver-heuristic.json ../input/downtown-vancouver.png ../output/
```

<br>**plot-on-map.py**

Args: `input-path`, `map-path`, `output-directory` \
Flags (optional): `-h` (heatmap based on heuristic) \
Returns: PNG image of data points plotted on the provided map. If no map is given, only prints the bounding box (coordinates of rectangular area containing all points), which can be used to download an appropriate map from `openstreetmap.org`.
```
$ python3 src/plot-on-map.py input/downtown-vancouver.json  # print bounding box
$ python3 src/plot-on-map.py input/downtown-vancouver.json input/downtown-vancouver.png output/  # basic scatterplot
$ python3 src/plot-on-map.py output/downtown-vancouver-heuristic.json input/downtown-vancouver.png output/ -h  # heatmap based on heuristic values
```
