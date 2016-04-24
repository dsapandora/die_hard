#!/usr/bin/env python

import roslib; roslib.load_manifest('DroneInteractiveEnviroment')
import rospy
from std_msgs.msg import String 
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata
class DieHard(object):
    def __init__(self):
        self.twist = Twist()
        rospy.init_node('DIEHARD')

        self.pub = rospy.Publisher('/cmd_vel', Twist, latch=True)
        rospy.Subscriber('/ardrone/navdata', Navdata, self.update_value)

    def update_value(self, msg):
        self.value = str(msg.vx) +" "+str(msg.vy)+" "+str(msg.vz)
        rospy.loginfo(self.value)


    def run(self):
        r = rospy.Rate(10)
        self.twist.linear.x = 0.30;                   # our forward speed
        self.twist.linear.y = 0; self.twist.linear.z = 0;     # we can't use these!        
        self.twist.angular.x = 0; self.twist.angular.y = 0;   #          or these!
        self.twist.angular.z = 0;                        # no rotation
        while not rospy.is_shutdown():
            self.pub.publish(self.twist)
            r.sleep()

if __name__=="__main__":
	DieHard().run()
