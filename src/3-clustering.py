import sys
import pandas as pd

from sklearn.cluster import KMeans

pd.options.mode.chained_assignment = None  # default='warn'


def main(input_path, output_path):
  # read input data
  points = pd.read_json(input_path, orient='records', lines=True)

  # get amenities whose heuristics are above a certain threshold
  top_amenities = points[points['interesting_heuristic'] >= 0.3]

  # cluster amenities by location
  X = top_amenities[['lat', 'lon']]
  model = KMeans(n_clusters=10)
  X['location_cluster'] = model.fit_predict(X)
  
  # write output
  points = pd.merge(points, X, on=['lat', 'lon'], how='left')
  points.to_json(output_path, orient='records', lines=True)
  

if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])