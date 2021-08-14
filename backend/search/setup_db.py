import pickle
import argparse
import glob
import cv2
from mysql.connector import MySQLConnection, Error, errorcode
from db_config import read_db_config
from descriptor import ColorDescriptor


def setup_db(args):
    db_config = read_db_config()
    conn = None

    try: 
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('Connection established')
            if args['init']:
                init_db(conn)
            if args['populate']:
                populate_db(conn,args['dataset'])
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

def init_db(conn):
    print('Initializing database...')
    cursor = conn.cursor()
    cursor.execute( 'DROP DATABASE IF EXISTS ImageSearch;')
    cursor.execute('CREATE DATABASE ImageSearch;')
    cursor.execute('USE ImageSearch;')
    cursor.execute( 'CREATE TABLE Images ('
                    'imgID INT NOT NULL AUTO_INCREMENT,'
                    'imgPath VARCHAR(60) NOT NULL,' 
                    'features BLOB,'
                    'PRIMARY KEY (imgID));'
                )
    conn.commit()
    print('Database initialized')

def populate_db(conn,dataset):
    print('Populating database...')
    cursor = conn.cursor()
    cursor.execute('USE ImageSearch;')

    imgs = glob.glob(dataset + '/*.jpg')
    imgs.extend(glob.glob(dataset + '/*.png'))

    BINS = (8,12,3)
    cd = ColorDescriptor(BINS)

    for imgPath in imgs:
        img = cv2.imread(imgPath)
        features = cd.get_features(img)
        pickled_features = pickle.dumps(features)

        cursor.execute("""INSERT INTO Images (imgPath,features) VALUES (%s,%s);""", (imgPath,pickled_features))

    conn.commit()
    print('Done populating database')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i','--init',action='store_true',help='Create database')
    ap.add_argument('-p','--populate',action='store_true',help='Add images to database')
    ap.add_argument('-d', '--dataset',required=False,help='Path to image dataset to be added to database')
    args = vars(ap.parse_args())

    if args['populate'] is True and args['dataset'] is None:
        raise Exception('Must pass path to dataset to populate table')

    setup_db(args)