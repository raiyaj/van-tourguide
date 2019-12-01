import sys
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

from math import radians, cos, sin, asin, sqrt


def reorder(points):
  # build an order that tries to minimize total haversine distance

  path = pd.DataFrame(columns=['lat', 'lon', 'amenity', 'tags', 'name'])  # empty dataframe
  addedIdxs = [] 

  for i in range(len(points)):
    if i == 0:
      # arbitrarily choose rightmost point as the first stop on the path
      rightmost = points[points['lon'] == points['lon'].max()]
      addedIdxs.append(rightmost.index[0])
      rightmost = rightmost.iloc[0]  # get first row from filter
      path = path.append({'lat': rightmost['lat'], 'lon': rightmost['lon'], 'amenity': rightmost['amenity'], 'tags': rightmost['tags'], 'name': rightmost['name']}, ignore_index=True)

    else:
      # of the remaining points, find nearest one to the prev point
      minDist = math.inf  # +infinity
      minIndex = -1
      prev = path.iloc[i-1]

      for j in range(len(points)):
        if j not in addedIdxs:
          curr = points.iloc[j]
          dist = haversine(prev['lon'], prev['lat'], curr['lon'], curr['lat'])
          
          if dist < minDist:
            minDist = dist
            minIndex = j

      # add nearest point to path
      nearest = points.iloc[minIndex]
      path = path.append({'lat': nearest['lat'], 'lon': nearest['lon'], 'amenity': nearest['amenity'], 'tags': nearest['tags'], 'name': nearest['name']}, ignore_index=True)
      addedIdxs.append(minIndex)

  return path


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

  return c * r * 1000 # to meters


def distance_walktime(path):
  # calculate total walking distance through the path
  walkDistance = 0

  for i in range(len(path) - 1):
    point1 = path.iloc[i]
    point2 = path.iloc[i+1]
    walkDistance += haversine(point1['lon'], point1['lat'], point2['lon'], point2['lat'])

  # print stats
  print("\nEstimated path length: " + str(round(walkDistance / 1000, 2)) + " km")
  # human walks 1.4m per second so
  print("Estimated walk time: " + str(math.floor((walkDistance / 1.4) / 60))  + " minutes" )


def main(input_path, output_dir):
  # read input data
  points = pd.read_json(input_path, orient='records', lines=True)

  # reorder points to minimize walking distance
  path = reorder(points)

  # print path
  print('Your path:')
  for i in range(len(path)):
    place = path.iloc[i]

    if 'website' in place['tags']:
      website = ' (' + place['tags']['website'] + ')'
    else:
      website = ''

    print(str(i+1) + '. ' + place['name'] + website)

  # print path stats
  distance_walktime(path)

  # write path
  path.to_json(output_dir.rstrip('/') + '/path.json', orient='records', lines=True)


if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])
