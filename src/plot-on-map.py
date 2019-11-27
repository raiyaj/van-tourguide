import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
  

def get_bounding_box(points, input_path):
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


def get_output_path(input_path, output_dir):
  filename = input_path.replace('.', '/').split('/')[-2]
  return f"{output_dir.rstrip('/')}/{filename}.png"


def create_plot(points, bounding_box, input_path, map_path, output_dir):
  # create fig and fit axes to bounding box
  fig, ax = plt.subplots()
  map = plt.imread(map_path)
  ax.set_xlim(bounding_box[0], bounding_box[1])
  ax.set_ylim(bounding_box[2], bounding_box[3])
  ax.ticklabel_format(useOffset=False)  # use real values instead of offset on x-axis


  # get flag if passed in
  if len(sys.argv) == 5:
    flag = sys.argv[4]
  else:
    flag = ''
  

  # plot data
  ax.imshow(map, extent=bounding_box)
  if not flag:
    plt.scatter(points.lon, points.lat, zorder=1, s=1)
  else:
    # sort by heuristic in ascending order so interesting pts plotted last
    points = points.sort_values(by='interesting_heuristic')

    # heuristic heatmap
    plt.scatter(points.lon, points.lat, zorder=1, c=points['interesting_heuristic'], s=points['interesting_heuristic']*8+0.2, cmap=plt.cm.cool)
    cbar = plt.colorbar()
    cbar.set_label("Custom 'interestingness' heuristic", rotation=270, labelpad=15)


  # add labels
  plt.title('Map of Input Coordinates')
  plt.xlabel('Longitude (\u00b0)')
  plt.ylabel('Latitude (\u00b0)')
  plt.xticks(rotation=20)

  plt.tight_layout()
  plt.savefig(get_output_path(input_path, output_dir), dpi=500)


def main(input_path):
  points = pd.read_json(input_path, orient='records', lines=True)

  # get bounding box
  bounding_box = get_bounding_box(points, input_path)

  if len(sys.argv) >= 4:
    # create plot
    map_path, output_dir = sys.argv[2:4]
    create_plot(points, bounding_box, input_path, map_path, output_dir)


if __name__ == '__main__':
  main(sys.argv[1])