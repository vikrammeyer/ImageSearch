import pickle
import argparse
from mysql.connector import MySQLConnection, Error, errorcode
from db_config import read_db_config
from descriptor import ColorDescriptor
import cv2 
import numpy as np

def search_db(args):
    db_config = read_db_config()
    conn = None

    try: 
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('Connection established')
            
            query_img = cv2.imread(args['query'])
            query_features = get_query_features(query_img)
            print('Searching...')
            results = None
            if args['limit'] is not None:
                results = search(conn,query_features,args['limit'])
            else:
                results = search(conn,query_features)
            print('Done searching...')
            cv2.imshow('Query', query_img)
            cv2.waitKey()

            for (dist, imgPath) in results:
                result = cv2.imread(imgPath)
                cv2.imshow('Result',result)
                cv2.waitKey()
            
        else:
            print('Connection failed')
    
    except Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Access Denied: Error with user name or password')
        else:
            print(e)

    finally: 
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed')

def get_query_features(query_img):
    BINS = (8,12,3)
    cd = ColorDescriptor(BINS)
    return cd.get_features(query_img)

def iter_row(cursor,size=10):
	""" Generator that chunks the database calls into a series of fetchmany() calls
			Args:
				cursor (cusor object): MySQLConnection Cursor object
				size (int): number of items to be returned in each fetchmany() call
	"""
	while True:
		rows = cursor.fetchmany(size)
		if not rows:
			break
		for row in rows:
			yield row

def search(conn,query_features,limit=10):
    results = {}
    cursor = conn.cursor()
    cursor.execute('USE ImageSearch;')
    cursor.execute('SELECT imgPath,features FROM Images;')

    for row in iter_row(cursor):
        imgPath, features = row[0], pickle.loads(row[1])        
        dist = chi_squared_dist(features,query_features)
        results[imgPath] = dist 
    
    results = sorted([(dist,path) for (path,dist) in results.items()])

    return results[:limit]

def chi_squared_dist(histA,histB,eps=1e-10):
    # As chi squared dist increases, the images are less similar
    # eps prevents division by zero errors
    return np.sum([((a-b)**2) / (a + b + eps) for (a,b) in zip(histA,histB)]) / 2

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-q','--query',required=True,help='Path to query image')
    ap.add_argument('-l','--limit',help='Number of similar images to return')
    args = vars(ap.parse_args())
    
    search_db(args)