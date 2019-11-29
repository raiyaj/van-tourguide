# Setup

## Required libraries
```
pandas
numpy
matplotlib
sklearn
```

## Running code

All scripts are in the `src/` directory, and scripts with a number in the filename should be executed in that order.


<br>**1-just-downtown-vancouver.py**

Args: `input-path`, `output-dir` \
Returns: JSON file containing only points that are roughly within Downtown Vancouver
```
$ python3 1-just-downtown-vancouver.py ../input/vancouver.json ../output/
```


<br>**2-interesting-heuristic.py**

Args: `input-path`, `output-dir` \
Returns: JSON file containing the same points, but with an added `interesting_heuristic` column (normalized to [0,1])
```
$ python3 2-interesting-heuristic.py ../output/downtown-van.json ../output/
```


<br>**3-clustering.py**

Args: `input-path`, `output-dir` \
Returns: JSON file containing the same points, but with an added `location_cluster` column (computed with KMeans clustering). If a point's heuristic is too low, `location_cluster` is `null`
```
$ python3 3-clustering.py ../output/heuristic.json ../output/
```


<br>**4-choose-places-to-visit.py**

Args: `input-path`, `output-dir` \
Returns: JSON file containing points to visit (decided based on a combination of cluster and heuristic)
```
$ python3 4-choose-places-to-visit.py ../output/clusters.json ../output/
```


<br>**5-distance.py**

Args: `input-path`, `image-path`,`output-directory` \
Returns: Estimated walking distance, estimated walking time, and veeery rough path to destination
```
$ python3 5-distance.py ../output/heuristic.json ../input/downtown-van.png ../output/
```


<br>**6-interesting-locations.py**

Args: `input-path`, `image-path`,`output-directory` \
Returns: A map with departure location, destination location, and some iteresting locations around the path 

```
$ python3 6-interesting-locations.py ../output/heuristic.json ../input/downtown-van.png ../output/
```

<br>**plot-on-map.py**

Args: `input-path`, `map-path`, `output-dir` \
Flags (optional): `-h` (heuristic heatmap), `-c` (clusters) \
Returns: PNG image of data points plotted on the provided map. If no map is given, only prints the bounding box (coordinates of rectangular area containing all points), which can be used to download an appropriate map from `openstreetmap.org`.
```
$ python3 plot-on-map.py ../output/downtown-van.json  # bounding box
$ python3 plot-on-map.py ../output/downtown-van.json ../input/downtown-van.png ../output/  # scatterplot
$ python3 plot-on-map.py ../output/heuristic.json ../input/downtown-van.png ../output/ -h
$ python3 plot-on-map.py ../output/clusters.json ../input/downtown-van.png ../output/ -c
```
