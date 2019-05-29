#!/usr/bin/env python

import sys
import rospy
import cv2

from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

def waypoint():
	position_publisher = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size = 10)
	rospy.init_node('first_challenge', anonymous = True)
	image_subscription = rospy.Subscriber('/iris_1/camera_down/image_raw', Image, bottom_video_callback);
	rate = rospy.Rate(10) # Hz
	while not rospy.is_shutdown():
		try:
			rate.sleep()
		except rospy.ROSInterruptException:
			pass
	cv2.destroyAllWindows()

def bottom_video_callback(data):
	try:
		cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
	except CvBridgeError as e:
		print(e)
	cv2.imshow("Bottom Camera", cv_image)
	cv2.waitKey(3) 

if __name__ == '__main__':
	waypoint()
	

 
