import sys
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
def slope(x1, y1, x2, y2):
    return (y2-y1)/(x2-x1)

def dist(x1, y1, x2, y2):
    dist =  math.sqrt(((x1 - x2)**2 + (y1 - y2)**2))
    return dist

def angle(x1, y1, x2, y2):
    return np.arctan2(y2 - y1, x2 -x1) - 0.6

def third_point(depLon, depLat, desLon, desLat):
    #Lat = y
    slp = dist(depLon, depLat, desLon, desLat)
    ang = angle(depLon, depLat, desLon, desLat)
    sideLine = slp*np.cos(ang)
    xMov = sideLine*np.cos(0.6)
    yMov = sideLine*np.sin(0.6)
    return(depLon + xMov, depLat + yMov)

def get_bounding_box(points):
  # Define bounding box (rectangular area that encompasses all data points).
  # Use coordinates to export map from openstreetmap.org

  min_lon = np.min(points.lon)
  max_lon = np.max(points.lon)
  min_lat = np.min(points.lat)
  max_lat = np.max(points.lat)

  print('Min lon:', min_lon)
  print('Max lon:', max_lon)
  print('Min lat:', min_lat)
  print('Max lat:', max_lat)

  return (min_lon, max_lon, min_lat, max_lat)
def plot_data(points, img_path, output_dir, xpoints, ypoints):
      bounding_box = get_bounding_box(points)
      fig, ax = plt.subplots()
      map = plt.imread(img_path)
      ax.set_xlim(bounding_box[0], bounding_box[1])
      ax.set_ylim(bounding_box[2], bounding_box[3])
      ax.ticklabel_format(useOffset=False)  # use real values instead of offset on x-axis
      #ax = plt.subplots()
      ax.imshow(map, extent=bounding_box)
      plt.scatter(xpoints[:2], ypoints[:2], zorder=1, s=20)
      plt.scatter(xpoints[2], ypoints[2], zorder=1, s=20, c = 'red')
      plt.plot([xpoints[0], xpoints[2]],[ypoints[0], ypoints[2]], 'k-')
      plt.plot([xpoints[1], xpoints[2]],[ypoints[1], ypoints[2]], 'k-')
      plt.savefig(output_dir + "distance.png")
#haversine function from Michael Dunn
#https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r * 1000 #to meters

def distance_walktime(xpoints, ypoints):
    firstWalk = haversine(xpoints[0], ypoints[0], xpoints[2], ypoints[2])
    secondWalk = haversine(xpoints[1], ypoints[1], xpoints[2], ypoints[2])
    walkDistance = firstWalk+secondWalk
    print("Distance to destinaiton is " + str(walkDistance) + "m")
    #human walks 1.4m per second so
    print("Estimated walk time is " + str(math.floor((walkDistance / 1.4) / 60))  + "minutes" )

def main(input_path, image_path, output_dir):
#def main():
  # read input data
  #points = pd.read_json(input_path, orient='records', lines=True)
  #input_path "../output/downtown-vancouver-heuristic.json"

  points = pd.read_json(input_path, orient='records', lines=True)

   #TEST path between Gastown and Commodore ballroom

  depLon= points['lon'][0] #Gastown
  depLat= points['lat'][0]
  desLon= points['lon'][1] #Commodore ballroom
  desLat= points['lat'][1]
  xpoints =  [depLon, desLon]
  ypoints =  [depLat, desLat]
  (thirLon, thirLat) = third_point(depLon,depLat,desLon,desLat)
  xpoints.append(thirLon)
  ypoints.append(thirLat)
  print(thirLon)
  print(thirLat)
  print(xpoints)
  print(ypoints)
  plot_data(points, image_path, output_dir, xpoints, ypoints)
  distance_walktime(xpoints, ypoints)



if __name__ == '__main__':
    #main()
    main(sys.argv[1], sys.argv[2], sys.argv[3]) #pass to json, pass to image, pass to output
