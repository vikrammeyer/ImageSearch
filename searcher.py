import numpy as np
import csv

class Searcher:
    def __init__(self,index_path):
        self.index_path = index_path

    def search(self,query_features,limit=10):
        results = {}

        with open(self.index_path) as f:
            reader = csv.reader(f)

            for row in reader:
                features = [float(x) for x in row[1:]]
                distance = self.chi_squared_dist(features,query_features)

                results[row[0]] = distance
            
        results = sorted([(dist,path) for (path,dist) in results.items()])
        
        return results[:limit]

    def chi_squared_dist(self,histA,histB,eps=1e-10):
        # Chi-sqaured dist of 0 -> histA and histB are identical
        # As chi squared dist increases, the images are less similar
        # eps prevents division by zero errors
        return np.sum([((a-b)**2) / (a + b + eps) for (a,b) in zip(histA,histB)]) / 2