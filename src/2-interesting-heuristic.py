import sys
import pandas as pd
import numpy as np
import requests

from sklearn.preprocessing import MinMaxScaler


def interesting_heuristic(amenity):
  # log progress
  global row_count
  row_count += 1
  if row_count % 100 == 0:
    print("Processing row " + str(row_count) + " ...")


  # detetermine interesting heuristic using a variety of factors
  heuristic = 0


  # boost score if amenity has wikidata (based on length of wiki entry)
  if 'wikidata' in amenity['tags'] or 'brand:wikidata' in amenity['tags']:
    wikitag = amenity['tags']['wikidata'] if 'wikidata' in amenity['tags'] else amenity['tags']['brand:wikidata']
    res = requests.get('https://www.wikidata.org/wiki/' + wikitag)
    
    if 'Content-Length' in res.headers and 'wikidata' in amenity['tags']:
      heuristic += int(res.headers['Content-Length']) / 100
      
    else:
      # problem with GET request, or amenity owned by a big brand; give approx. avg length
      heuristic += 30
    
  
  # adjust score depending on tags
  with open('src/boring-amenities.txt', 'r') as f:  # read list of boring amenities
    boring_amenities = f.read().splitlines()
    
    # lower score of boring amenities and chain restaurants
    if amenity['amenity'] in boring_amenities or 'brand' in amenity['tags']:
      heuristic -= 100
    
    else:
      # boost score if amenity has certain tags
      if any(t in amenity['tags'] for t in ['leisure', 'tourism']):
        heuristic += 70
      
      # boost score of food-related amenities with lots of tags
      if amenity['amenity'] in ['bar', 'cafe', 'ice_cream', 'pub', 'restaurant']:
        if len(amenity['tags']) >= 8:
          heuristic += 40


  return heuristic


def uniqueness_adjustment(points):
  # boost score if amenity type is unique
  amenity_groups = points.groupby('amenity').size().to_frame(name='duplicate_amenity_count')
  max_duplicates = np.max(amenity_groups['duplicate_amenity_count'])
  points = points.join(amenity_groups, on='amenity')
  points['interesting_heuristic'] += (max_duplicates / points['duplicate_amenity_count']) / 10

  # lower score if amenity name is not unique
  name_groups = points.groupby('name').size().to_frame(name='duplicate_name_count')
  points = points.join(name_groups, on='name')
  points['interesting_heuristic'] /= points['duplicate_name_count']

  return points


def main(input_path, output_dir):
  # read input data
  points = pd.read_json(input_path, orient='records', lines=True)

  # determine interesting heuristic of each amenity
  global row_count  # global var for logging progress of HTTP calls
  row_count = 0
  points['interesting_heuristic'] = points \
    .dropna(subset=['name']) \
    .apply(interesting_heuristic, axis=1)

  # adjust heuristics based on amenity uniqueness (more interesting if more unique)
  points = uniqueness_adjustment(points)
  
  # normalize heuristic values to be in [0,1]
  scaler = MinMaxScaler()
  points['interesting_heuristic'] = scaler.fit_transform(points[['interesting_heuristic']])

  # write data to output file
  # output_path = f"{output_dir.rstrip('/')}/{input_path.replace('.', '/').split('/')[-2]}-heuristic.json"
  points \
    .fillna({'interesting_heuristic':0}) \
    .sort_values(by='interesting_heuristic', ascending=False) \
    .to_json("output_dir.rstrip('/')"+"/"+input_path.replace('.', '/').split('/')[-2]+"-heuristic.json", orient='records', lines=True)


if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])