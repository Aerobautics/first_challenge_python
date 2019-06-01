#!/usr/bin/env python

import sys
import rospy
import cv2
import numpy as np, cv2

from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

sd_height = 480
sd_width = 858
image_channels = 3
bridge = CvBridge()
#cv_image = cv.CreateMat(sd_height, sd_width, cv2.CV_32FC3)
cv_image = np.zeros([sd_height, sd_width, image_channels])
local_position = PoseStamped()
pause_length = 100

def mainfunction():
	local_position = PoseStamped()
	state = State()
	service_timeout = 30
	rospy.loginfo("Waiting for ROS services . . .")
	try:
		rospy.wait_for_service('mavros/param/get', service_timeout)
		rospy.wait_for_service('mavros/cmd/arming', service_timeout)
		rospy.wait_for_service('mavros/mission/push', service_timeout)
		rospy.wait_for_service('mavros/mission/clear', service_timeout)
		rospy.wait_for_service('mavros/set_mode', service_timeout)
		rospy.loginfo("Desired ROS services are available.")
	except rospy.ROSException:
		print "Failed to connect to services."	
	
def waypoint():
	elapsed_time = 0
	mainfunction()
	position_publisher = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size = 10)
	position_subscriber = rospy.Subscriber('mavros/local_position/pos', PoseStamped, position_callback)
	state_subscriber = rospy.Subscriber('mavros/state', State, state_callback)
	rospy.init_node('first_challenge', anonymous = True)
	image_subscription = rospy.Subscriber('/iris_1/camera_down/image_raw', Image, bottom_video_callback);
	rate = rospy.Rate(10) # Hz
	while not rospy.is_shutdown():
		try:
			rate.sleep()
		except rospy.ROSInterruptException:
			pass
		elapsed_time += 1;
		if (elapsed_time > pause_length):
			elapsed_time = 0
			print "Current position: (", local_position.pose.position.x, ", ", local_position.pose.position.y, ", ", local_position.pose.position.z, ")"
	cv2.destroyAllWindows()

def bottom_video_callback(data):
	try:
		cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
	except CvBridgeError as e:
		print(e)
	cv2.imshow("Bottom Camera", cv_image)
	cv2.waitKey(3) 

def position_callback(data):
	local_position = data

def state_callback(data):
	state = data;

if __name__ == '__main__':
	waypoint()
	

 
