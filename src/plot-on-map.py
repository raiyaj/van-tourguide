import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Ellipse


BOUNDING_BOX_TEMPLATE = (
  "Min. longitude: {bounding_box[0]}\n"
  "Max. longitude: {bounding_box[1]}\n"
  "Min. latitude: {bounding_box[2]}\n"
  "Max. latitude: {bounding_box[3]}"
)


def get_bounding_box(points):
  # Define bounding box (rectangular area that encompasses all data points).
  # Use coordinates to export map from openstreetmap.org
  return (np.min(points.lon), np.max(points.lon), np.min(points.lat), np.max(points.lat))


def draw_clusters(points, ax):
  num_clusters = points['location_cluster'].nunique()
  
  # draw an ellipse around each cluster of points
  for i in range(num_clusters):
    # get ellipse's center (x,y) coordinate, width, and height
    cluster_bbox = get_bounding_box(points[points['location_cluster'] == i])
    ellipse_center_x = (cluster_bbox[0] + cluster_bbox[1]) / 2
    ellipse_center_y = (cluster_bbox[2] + cluster_bbox[3]) / 2
    ellipse_width = abs(cluster_bbox[1] - cluster_bbox[0]) + 0.0015
    ellipse_height = abs(cluster_bbox[3] - cluster_bbox[2]) + 0.0015

    # draw ellipse
    ellipse = Ellipse(
      (ellipse_center_x, ellipse_center_y),
      ellipse_width,
      ellipse_height,
      color='#6d89fc',
      linewidth=0,
      alpha=0.4
    )
    ax.add_artist(ellipse)


def draw_path(path):
  # draw n-1 lines to connect the points
  for i in range(len(path) - 1):
    pair = path.iloc[i:i+2]  # rows i and i+1
    plt.plot(pair['lon'], pair['lat'], color='#1065de', alpha=0.8, linewidth=1.5, zorder=1)


def get_plot_title(flag):
  if flag == '-h':
    return "Input coordinates, coloured by 'interestingness'"
  elif flag == '-c':
    return 'Most interesting coordinates, clustered'
  elif flag == '-p':
    return 'Haversine path of city tour'
  else:
    return 'Input coordinates'


def get_output_path(output_dir, flag):
  if not flag:
    filename = 'scatterplot'
  elif flag == '-h':
    filename = 'heuristic'
  elif flag == '-c':
    filename = 'clusters'
  elif flag == '-p':
    filename = 'path'

  return f"{output_dir.rstrip('/')}/{filename}.png"
  

def create_plot(points, bounding_box, input_path, map_path, path_path, output_dir, flag):
  # create fig and fit axes to bounding box
  fig, ax = plt.subplots()
  map = plt.imread(map_path)
  ax.set_xlim(bounding_box[0], bounding_box[1])
  ax.set_ylim(bounding_box[2], bounding_box[3])
  ax.ticklabel_format(useOffset=False)  # use real values instead of offset on x-axis
  

  # plot map as background image
  ax.imshow(map, extent=bounding_box)  # draw map
  

  # basic scatterplot
  if not flag:
    plt.scatter(points.lon, points.lat, zorder=1, s=1)
  
  else:
    if flag == '-c' or flag == '-p':
      # ignore points w/ null cluster number
      points = points.dropna(subset=['location_cluster'])
      draw_clusters(points, ax)
  
      if flag == '-p':
        # draw path
        path = pd.read_json(path_path, orient='records', lines=True)
        draw_path(path)
      

    # sort by heuristic in ascending order so interesting pts plotted last
    points = points.sort_values(by='interesting_heuristic')

    # heuristic-based heatmap
    plt.scatter(
      points.lon,
      points.lat,
      zorder=2,
      c=points['interesting_heuristic'],
      s=points['interesting_heuristic']*8+0.2,  # add constant so pts w/ h=0 are plotted too
      cmap=plt.cm.cool
    )
    cbar = plt.colorbar()
    cbar.set_label('Heuristic value', rotation=270, labelpad=15)


  # add labels
  plt.title(get_plot_title(flag))
  plt.xlabel('Longitude (\u00b0)')
  plt.ylabel('Latitude (\u00b0)')


  # fix layout
  plt.locator_params(nbins=4)  # set number of ticks
  plt.tight_layout()
  if 'downtown-van' in map_path:
    ax.set_aspect(1.25)  # stretch map vertically


  # save fig
  plt.savefig(get_output_path(output_dir, flag), dpi=500)


def main(input_path):
  # read input data
  points = pd.read_json(input_path, orient='records', lines=True)


  # get bounding box
  bounding_box = get_bounding_box(points)


  if len(sys.argv) < 4:
    print(BOUNDING_BOX_TEMPLATE.format(bounding_box=bounding_box))

  else:
    # extract command-line args
    if len(sys.argv) <= 5:
      map_path, output_dir = sys.argv[2:4]
      path_path = ''
      
      if len(sys.argv) == 5:
        flag = sys.argv[4]
      else:
        flag = ''
    
    else:
      path_path, map_path, output_dir = sys.argv[2:5]
      flag = sys.argv[5]
  

    # create plot
    create_plot(points, bounding_box, input_path, map_path, path_path, output_dir, flag)


if __name__ == '__main__':
  main(sys.argv[1])