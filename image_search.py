from descriptor import ColorDescriptor
from searcher import Searcher

import argparse
import cv2 

ap = argparse.ArgumentParser()
ap.add_argument('-i','--index',required=True,help='Path where computed index will be stored')
ap.add_argument('-q','--query',required=True,help='Path to query image')

args = vars(ap.parse_args())

BINS = (8,12,3)
cd = ColorDescriptor(BINS)

query = cv2.imread(args['query'])
query_features = cd.get_features(query)
searcher = Searcher(args['index'])
print('Searching...')
results = searcher.search(query_features)
print('Done searching')
cv2.imshow('Query',query)
cv2.waitKey()

for (dist,imgPath) in results:
    result = cv2.imread(imgPath)
    cv2.imshow('Result',result)
    cv2.waitKey()