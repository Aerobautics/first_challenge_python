#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

def waypoint():
	pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size = 10)
	rospy.init_node('first_challenge', anonymous = True)
	rate = rospy.Rate(10) # Hz
	while not rospy.is_shutdown():
		try:
			rate.sleep()
		except rospy.ROSInterruptException:
			pass

 
