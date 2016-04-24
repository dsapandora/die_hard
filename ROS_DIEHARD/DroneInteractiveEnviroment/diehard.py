#!/usr/bin/env python

import roslib; roslib.load_manifest('DroneInteractiveEnviroment')
import rospy
import json
import requests
from std_msgs.msg import String 
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata


class DieHard(object):
    def __init__(self):
        self.twist = Twist()
        rospy.init_node('DIEHARD')

        self.pub = rospy.Publisher('/cmd_vel', Twist, latch=True)
        rospy.Subscriber('/ardrone/navdata', Navdata, self.update_value)
        self.twist.linear.x = 0;                   # our forward speed
        self.twist.linear.y = 0; 
        self.twist.linear.z = 0;     # we can't use these!        
        self.twist.angular.x = 0; self.twist.angular.y = 0;   #          or these!
        self.twist.angular.z = 0;   

    def update_value(self, msg):
        self.value = str(msg.vx) +" "+str(msg.vy)+" "+str(msg.vz)
        response = requests.get('http://10.100.100.104:5000/am_gonna_die?longitude=%s&latitude=%s&elevation=%s' % (msg.vx, msg.vy, msg.vz))
        rospy.loginfo(self.value)
        value  = json.loads(response.text)
        rospy.loginfo(value)
        rospy.loginfo("response:"+ str(value['distance'])+" "+str(value['latitude'])+" "+str(value['longitude']))
        self.twist.linear.x = float(value['latitude']*float(value['distance']))
        self.twist.linear.y = float(value['longitude']*float(value['distance']))
        
    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.pub.publish(self.twist)
            r.sleep()

if __name__=="__main__":
	DieHard().run()
