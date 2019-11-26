import sys
import pandas as pd


def main(input_path, output_dir):
  points = pd.read_json(input_path, orient='records', lines=True)

  # keep points in Downtown Vancouver only
  points = points[
    (points['lon'] >= -123.1466) &
    (points['lon'] <= -123.1018) &
    (points['lat'] >= 49.2700) &
    (points['lat'] <= 49.2953)
  ]

  points.to_json(output_dir.rstrip('/') + '/downtown-vancouver.json', orient='records', lines=True)


if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])