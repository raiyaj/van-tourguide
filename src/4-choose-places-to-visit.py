import sys
import pandas as pd
import numpy as np


def main(input_path, output_path):
  # read input data
  points = pd.read_json(input_path, orient='records', lines=True)


  # get the most interesting amenity from each cluster

  # step 1: get each cluster's max heuristic value
  max_cluster_heuristics = points \
    .dropna(subset=['location_cluster']) \
    .groupby('location_cluster')['interesting_heuristic'].max() \
    .reset_index(name='interesting_heuristic')
  
  # step 2: join on both variables to filter out amenities whose 
  # heuristic != max heuristic in its cluster
  candidates = pd.merge(points, max_cluster_heuristics, on=['location_cluster', 'interesting_heuristic'], how='inner')
  candidates.drop_duplicates('location_cluster', inplace=True)


  # keep randomly choosing groups of places until we get a combination where all
  # amenities have different types
  num_clusters = candidates['location_cluster'].nunique()
  num_places_to_visit = 7

  while True:
    # get random cluster numbers
    rand_clusters = np.random.choice(
      np.arange(num_clusters),
      size=num_places_to_visit,
      replace=False  # without replacement, so no repeats
    )
    
    # get the places in those clusters
    places_to_visit = candidates[candidates['location_cluster'].isin(rand_clusters)]
    
    # if combo has enough variety, output places to visit
    if places_to_visit['amenity'].is_unique:
      places_to_visit.to_json(output_path, orient='records', lines=True)
      break


if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])