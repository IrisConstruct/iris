import numpy as np
import cv2
from math import sqrt, pow, acos

def rotate(imgl, key1, key2, matches):
    x1, y1 = key1[matches[1].queryIdx].pt
    x2, y2 = key1[matches[2].queryIdx].pt
    x3, y3 = key2[matches[1].trainIdx].pt
    x4, y4 = key2[matches[2].trainIdx].pt

    dotproduct = ((x2-x1)*(x4-x3)) + ((y2-y1)*(y4-y3))
    dist_l = sqrt(pow((x2-x1),2) + pow((y2-y1),2))
    dist_r = sqrt(pow((x4-x3),2) + pow((y4-y3),2))
    cos_theta = dotproduct/(dist_l*dist_r)
    theta = acos(cos_theta)
    theta = (theta/3.14159265359)*180
    
    rowsl,colsl = imgl.shape
    M = cv2.getRotationMatrix2D((colsl/2, rowsl/2), theta, 1)
    dst = cv2.warpAffine(imgl, M, (colsl,rowsl))
    return dst, theta

def analyze(key1, key2, matches, scale): 
    x1, y1 = key1[matches[0].queryIdx].pt
    x2, y2 = key2[matches[0].trainIdx].pt
    x1, y1 = x1*scale[0], y1*scale[1]
    return x2-x1, y2-y1

def scale(key1, key2, matches, amount):
    x1, y1 = key1[matches[0].queryIdx].pt
    x2, y2 = key1[matches[1].queryIdx].pt
    x3, y3 = key2[matches[0].trainIdx].pt
    x4, y4 = key2[matches[1].trainIdx].pt
    totalx = abs(x2-x1)/abs(x4-x3)
    totaly = abs(y2-y1)/abs(y4-y3)
    print totalx, totaly
    return totalx, totaly

def score(first, second):
    alpha = cv2.imread(first["path"], 0)
    beta = cv2.imread(second["path"], 0)
    
    # Initiate the SIFT detector
    orb= cv2.ORB()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(alpha, None)
    kp2, des2 = orb.detectAndCompute(beta, None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match Descriptors
    matches = bf.match(des1, des2)

    #Sort them in order of distance
    matches = sorted(matches, key = lambda x:x.distance)
    
    alpha, angle = rotate(alpha, kp1, kp2, matches)

    # Initiate the SIFT detector
    orb= cv2.ORB()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(alpha, None)
    kp2, des2 = orb.detectAndCompute(beta, None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match Descriptors
    matches = bf.match(des1, des2)

    #Sort them in order of distance
    matches = sorted(matches, key = lambda x:x.distance)
    
    imgscale = scale(kp1, kp2, matches, 1)
    return analyze(kp1, kp2, matches, imgscale)
