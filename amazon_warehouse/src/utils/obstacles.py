#!/usr/bin/env python
import threading
import os
from random import random
import rospy
from geometry_msgs.msg import Pose2D
from math import sqrt, pow

class Obstacles():

    def manageObstacles(self):
        print("Management of obstacles starting")
        obstacle = False
        pose1 = Pose2D()
        pose1.x = 3
        pose1.y = -4
        while(True):
            r = random()
            if (obstacle == False and r > 0.5):
                if sqrt(pow((self.pose.x - pose1.x), 2) + pow((self.pose.y - pose1.y), 2)) > 2:
                    os.system('rosrun gazebo_ros spawn_model -file /home/user/catkin_ws/src/amazon_warehouse/models/obstacle/model.sdf -sdf -x ' + str(pose1.x) + ' -y ' + str(pose1.y) + ' -z ' + str(pose1.theta) + ' -model obstacle')
                    obstacle = True
            elif obstacle == True and r > 0.5:
                os.system('rosservice call gazebo/delete_model \'{model_name: obstacle}\'')
                obstacle = False
            rospy.sleep(10)

    def __init__(self, pose):
        self.pose = pose
        self.thread = threading.Thread(target=self.manageObstacles)
        self.thread.start()
    
