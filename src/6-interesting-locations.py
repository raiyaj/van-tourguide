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
      print(len(xpoints))
      plt.scatter(xpoints[0:len(xpoints) ], ypoints[0:len(ypoints)], zorder=1, s=20, c='blue', label = "departure and destination")
      plt.scatter(xpoints[1:len(xpoints) -1], ypoints[1:len(ypoints)-1], zorder=1, s=20, c='red', label ="interesting locations on the path")
      #plt.scatter(xpoints[], ypoints[0], zorder=1, s=20, c = 'red')
      #plt.plot([xpoints[0], xpoints[2]],[ypoints[0], ypoints[2]], 'k-')
      #plt.plot([xpoints[1], xpoints[2]],[ypoints[1], ypoints[2]], 'k-')

      plt.savefig(output_dir + "distance-general.png")
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

  points = pd.read_json(input_path, orient='records', lines=True)
  #Sort the points with latitude and lonitude so each neighbor rows will be points that are close to each other
  sorted_points = points.sort_values(['lat', 'lon']).reset_index()

  #TEST path between Gastown and Commodore ballroom
  depLon= points['lon'][0] #Gastown
  depLat= points['lat'][0]
  desLon= points['lon'][1] #Commodore Ballroom
  desLat= points['lat'][1]
  #get the index of departure location and destination location
  depIdx = sorted_points[(sorted_points['lon'] == depLon) & (sorted_points['lat'] == depLat)].index
  desIdx = sorted_points[(sorted_points['lon'] == desLon) & (sorted_points['lat'] == desLat)].index

  #get the # of rows so we won't exceed it
  numRows = sorted_points.shape[0]
  #maxChecking = numRows -6

  #path array that will contain indexes of each ro
  pathArr = []
  checkedIdx = []
  idx = depIdx[0] #Start with the departure index depIdx1706, desIdx 1017
  direction = 0
  #if desIdx[0] > depIdx[0]:
  pathArr.append(idx)
  checkedIdx.append(idx)
  depDesDist =  haversine(sorted_points.iloc[depIdx[0]]['lon'], sorted_points.iloc[depIdx[0]]['lat'], sorted_points.iloc[desIdx[0]]['lon'], sorted_points.iloc[desIdx[0]]['lat'])
  while idx != desIdx[0]:
      #We will check the
      startIdx = idx - 10
      endIdx = idx + 10
      if startIdx < 0:
          startIdx = 0
      elif idx >= numRows -1:
          endIdx = numRows -1
      #calculate the distance between our examining location and destination
      minDist =  haversine(sorted_points.iloc[startIdx]['lon'], sorted_points.iloc[startIdx]['lat'], sorted_points.iloc[desIdx[0]]['lon'], sorted_points.iloc[desIdx[0]]['lat'])
      minIndex = startIdx
      checkedIdx.append(minIndex)
      for i in range(startIdx + 1, endIdx + 1):
          if i in checkedIdx:
              continue
          #calculate the distance to destination for each locations
          dist = haversine(sorted_points.iloc[i]['lon'], sorted_points.iloc[i]['lat'], sorted_points.iloc[desIdx[0]]['lon'], sorted_points.iloc[desIdx[0]]['lat'])
          if dist <= minDist:
              minDist = dist
              minIndex = i
          checkedIdx.append(i)
          #print(dist)
      idx = minIndex
      tempDist = haversine(sorted_points.iloc[idx]['lon'], sorted_points.iloc[idx]['lat'], sorted_points.iloc[desIdx[0]]['lon'], sorted_points.iloc[desIdx[0]]['lat'])
      if(tempDist <= depDesDist):
          pathArr.append(idx)
      #print(idx)
  print(pathArr)
  #sorted_points = sorted_points.iloc[pathArr][sorted_points.iloc[pathArr]['interesting_heuristic'] > 0.5]
  xpoints = sorted_points.iloc[pathArr]['lon']
  ypoints = sorted_points.iloc[pathArr]['lat']
  heuristics = sorted_points.iloc[pathArr]['interesting_heuristic'] > 0.3
  #print(xpoints[heuristics])
  #print(heuristics)

  plot_data(points, image_path, output_dir, xpoints[heuristics], ypoints[heuristics])





if __name__ == '__main__':
    #main()
    main(sys.argv[1], sys.argv[2], sys.argv[3]) #pass to json, pass to image, pass to output
