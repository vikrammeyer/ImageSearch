# Image Search Overview
This project implements a search function for similar images based on an input image. Images are stored on the disk and a MySQL database stores the path to the images and the feature vector that describes the images and is used to determine how similar images are to each other. A command line interface built with argparse is used to setup the database and search for similar images.

## Setting up and Running Image Search
1. Download the 1.1 GB [INRIA holiday dataset](http://lear.inrialpes.fr/people/jegou/data.php#holidays) to the project's root directory 
   - Any sufficiently large dataset of images can be used (e.g. Food, Clothing, etc.) instead of the holiday dataset
2. Create a python virtual environment and do `pip install -r requirements.txt` to install OpenCV, Numpy, and the MySQL Connector
3. Ensure MySQL is installed and the login details are provided in `config.ini`
   - The `config.ini` file should follow the following format:  
      ``` 
      [mysql]
      host = localhost
      user = root
      password = test123
      ```
   - Can connect to MySQL running on a remote server by supplying the server's address for host
4. Run `setup_db.py` to create the MySQL ImageSearch database and the Images table. (Run only once for initial setup)
   - Run in terminal: `python3 setup_db.py --init --populate --dataset images_folder` in order to initialize the database and populate the Images table with the image paths and their feature arrays pickled and stored as BLOBs
5. Run `search_db.py` to find similar images to the passed in image (Can run as many times as desired)
   - Run in terminal: `python3 search_db.py --query image_path`
   - Can add `--limit 5` to limit the number of results to a specific number (default is 10) 