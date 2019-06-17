import argparse

parser = argparse.ArgumentParser()
parser.add_argument('trained_model')
parser.add_argument('detect_dir')
parser.add_argument('outpath')
args = parser.parse_args()


