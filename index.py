from descriptor import ColorDescriptor
import argparse
import glob
import cv2
import csv

ap = argparse.ArgumentParser()
ap.add_argument('-i','--index',required=True,help='Path to where index will be stored')
ap.add_argument('-d','--dataset',required=True,help='Path to directory with images to be indexed')

args =vars(ap.parse_args())

BINS = (8,12,3)

cd = ColorDescriptor(BINS)

with open(args['index'],'w') as f:
    writer = csv.writer(f)
    print('Start indexing...')
    for imgPath in glob.glob(args['dataset'] + '/*.jpg'):
        img = cv2.imread(imgPath)
        features = cd.get_features(img)
        row = [imgPath]
        row.extend(features)
        writer.writerow(row)
    print('Done indexing')