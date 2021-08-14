import numpy as np
import cv2

class ColorDescriptor:
    def __init__(self,bins):
        self.bins = bins # 3 element tuple 
    
    def get_features(self,image):
        img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        h, w = img.shape[:2]
        cX, cY = int(w / 2), int(h /2)
        features = []
        segments = [(0,0,cX,cY),(cX,0,w,cY),(0,cY,cX,h),(cX,cY,w,h)]

        # Ellipse will be 70% height of img
        x_length = int(w * 0.7) // 2
        y_length = int(h * 0.7) // 2
        axes_length = (x_length,y_length)
        
        # White ellipse on black background 
        ellipse_mask = cv2.ellipse(np.zeros((h,w),dtype='uint8'),(cX,cY),axes_length,0,0,360,255,-1)

        for (x1,y1,x2,y2) in segments:
            corner_mask = cv2.rectangle(np.zeros((h,w),dtype='uint8'), (x1,y1), (x2,y2), 255, -1)
            corner_mask = cv2.subtract(corner_mask,ellipse_mask)
            
            corner_histogram = self.histogram(img,corner_mask)
            features.extend(corner_histogram)

        ellipse_histogram = self.histogram(img,ellipse_mask)
        features.extend(ellipse_histogram)

        return features

    def histogram(self,image,mask):
        hist = cv2.calcHist([image],[0,1,2],mask,self.bins,[0,256,0,256,0,256])
        hist = cv2.normalize(hist,hist).flatten()
        return hist    