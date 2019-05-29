# -*- coding: utf-8 -*-
"""
Created on Fri May 24 13:27:34 2019

@author: e360568
"""
#Import:Libraries(including clusters)
import os
import cv2
import math
import win32com
import numpy as np
#import roslibpy
import rospy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from numpy.linalg import lstsq
from matplotlib import pyplot as plt

from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
from sklearn.linear_model import LinearRegression

def callback_function(input):
	print("")

def process_image():
	rospy.init_node('find_centroids', anonymous = True)
	rospy.Subscriber('/iris_1/camera_down/image_raw', Image, callback)
	rospy.spin()

#Distance Formula
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

###############################################################################
#Load:Query image
apriltag_query_path = r"C:\Users\e360568\Desktop\hack\apriltag.JPG"

#Load:Apriltag in frame
apriltag_frame_path = r"C:\Users\e360568\Desktop\hack\screenshot.JPG"

def find_centroids(apriltag_query_path, apriltag_frame_path):
    apriltag_query = cv2.imread(apriltag_query_path,0)
    apriltag_frame = cv2.imread(apriltag_frame_path, 0)    

    #Task:Initiate SIFT detector
    orb = cv2.ORB_create()

    #Task:Find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(apriltag_query,None)
    kp2, des2 = orb.detectAndCompute(apriltag_frame,None)

    #Task:Create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    #Task:Match descriptors.
    matches_ = bf.match(des1,des2)

    #Task:Sort them in the order of their distance.
    matches = sorted(matches_, key = lambda x:x.distance)
    good_matches = matches[:7]
    
    #Task:Get coordinates of all those matches(keypoints) in the frame
    list_kp1 = [kp1[mat.queryIdx].pt for mat in good_matches]
    temp_list_kp2 = [kp2[mat.trainIdx].pt for mat in good_matches]
    #print(temp_list_kp2)

    temp_dat = []
    for i in temp_list_kp2:
        temp_dat.append(apriltag_frame.shape[0]-i[1])

    list_kp2 = []
    for kp,temp in zip(temp_list_kp2,temp_dat):
        list_kp2.append((kp[0],temp))

    #Task:Make accessible lists for x and y coordinates
    x = np.array([int(item[0]) for item in list_kp2])
    y = np.array([int(item[1]) for item in list_kp2])
    X = np.array(list(zip(x,y))).reshape(len(x), 2)

    ###READ:UNSUPERVISED LEARNING METHOD
    #Task:Apply kmeans method to determine optimal k number of clusters in frame
    distortions = []
    K = range(1,len(X)+1)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

    #Get list of all the points on elbow plot; Get points at min(k) and max(k)
    k_points = []
    for k,d in zip(K,distortions):
        k_points.append((k,d))
        point1 = k_points[0]
        point2 = k_points[-1]
    
    #Task:Use elbow to find out optimal k
    temp_lst = (point1,point2)
    #Subtask 1: Get all x values and y values
    x_vals = np.array([item[0] for item in temp_lst]).reshape(-1,1)
    y_vals = np.array([item[1] for item in temp_lst]).reshape(-1,1)
    #Subtask 2: Create linear model and fit
    linear_regressor = LinearRegression()
    linear_regressor.fit(x_vals,y_vals)
    #Subtask 3: Use model to predict all values of k
    y_pred = []
    for k in K: 
        y_pred.append(linear_regressor.intercept_ + linear_regressor.coef_ * k)
        
    temp_points = np.array(y_pred).ravel()

    y_pred_points = []
    for k,p in zip(K,temp_points):
        y_pred_points.append((k,p))

    #Subtask 3: Find distance between all the elbow points and the points on line
    distances = []
    for k_pts,y_pts in zip(k_points,y_pred_points):
        distances.append(distance(k_pts,y_pts))
        
    #Subtask 4: OptK is the associated k-value of the max distance
    opt_k = []
    for k,d in zip(K,distances):
        if d == max(distances):
            opt_k = k

    #Task:Use optimal k to create the clusters
    kmeans_model = KMeans(n_clusters=opt_k).fit(X)

    #Task:Find the centroids of those clusters
    centers = np.array(kmeans_model.cluster_centers_)
    print(centers)
    
    return centers
    
