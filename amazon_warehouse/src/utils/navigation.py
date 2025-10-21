#!/usr/bin/env python
import obstacles
import rospy
from geometry_msgs.msg import Pose2D, Twist, Point, Quaternion
from std_msgs.msg import Float32
from math import radians, copysign, sqrt, pow, pi, atan2
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class Navigation():

    def __init__(self):
        self.obstacles = False
        self.current_pose = Pose2D()
        self.true_pose = Pose2D()
        self.goal_pose = Pose2D()
        self.goal_pose.x = -6
        self.goal_pose.y = 2
        self.rotations = 0

        # Starts a new node
        rospy.init_node('amazon_warehouse_robot', anonymous=True)

        # Publishers
        self.velocity_publisher = rospy.Publisher('/amazon_warehouse_robot/cmd_vel', Twist, queue_size=10)
        self.prismatic_publisher = rospy.Publisher('/amazon_warehouse_robot/joint_cmd', Float32, queue_size=10)
        
        # Subscriptions
        rospy.Subscriber('/amazon_warehouse_robot/odom',Odometry,self.odometryCb)
        rospy.Subscriber('/ground_truth/state',Odometry,self.groundTruthCb) # True state of the robot

        if self.obstacles:
            obs = obstacles.Obstacles(self.current_pose)

        rospy.sleep(1)

    def odometryCb(self,msg):
        self.current_pose.x = msg.pose.pose.position.x
        self.current_pose.y = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        self.current_pose.theta = yaw

    def groundTruthCb(self,msg):
        self.true_pose.x = msg.pose.pose.position.x
        self.true_pose.y = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        self.true_pose.theta = yaw

    def upLift(self):
        print("UP LIFT")

        # Check orientation
        r = rospy.Rate(10)
        vel_msg = Twist()
        while(abs(abs(self.goal_pose.theta) - abs(self.current_pose.theta)) > 0.1):
            if self.current_pose.theta > self.goal_pose.theta:
                vel_msg.angular.z = -0.2
            else:
                vel_msg.angular.z = 0.2
            self.velocity_publisher.publish(vel_msg)
            r.sleep()
        #After the loop, stops the robot
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        rospy.sleep(1)
        
        # Up lift
        i = 0
        while(i < 10):
            self.prismatic_publisher.publish(Float32(25))
            r.sleep()
            i = i + 1
        rospy.sleep(1)

    def downLift(self):
        print("DOWN LIFT")

        # Check orientation
        vel_msg = Twist()
        r = rospy.Rate(10)
        while(abs(abs(self.goal_pose.theta) - abs(self.current_pose.theta)) > 0.1):
            if self.current_pose.theta > self.goal_pose.theta:
                vel_msg.angular.z = -0.2
            else:
                vel_msg.angular.z = 0.2
            self.velocity_publisher.publish(vel_msg)
            r.sleep()
        #After the loop, stops the robot
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        rospy.sleep(1)

        # Down lift
        i = 0
        while(i < 10):
            self.prismatic_publisher.publish(Float32(0))
            r.sleep()
            i = i + 1
        rospy.sleep(1)

    def move(self,distance):
        print("MOVE ", distance)
        goal_x = self.goal_pose.x
        goal_y = self.goal_pose.y
        if self.rotations == 0:
            goal_x = goal_x + distance
        elif self.rotations == 1:
            goal_y = goal_y + distance
        elif self.rotations == 2:
            goal_x = goal_x - distance
        elif self.rotations == 3:
            goal_y = goal_y - distance

        self.moveToGoal(goal_x,goal_y)        

    def moveToGoal(self,goal_x,goal_y):
        movement = self.classifyMovement(goal_x, goal_y)
        self.goal_pose.x = goal_x
        self.goal_pose.y = goal_y
        r = rospy.Rate(3)
        vel_msg = Twist()
        current_distance = 100
        #Loop to move the robot at a specified goal
        while(current_distance > 0.1):
            inc_x = goal_x - self.current_pose.x
            inc_y = goal_y - self.current_pose.y

            angle_to_goal = atan2(inc_y, inc_x)

            if abs(abs(angle_to_goal) - abs(self.current_pose.theta)) > 0.1: # Check angle with goal
                vel_msg.linear.x = 0.0

                if (angle_to_goal < 0 and self.current_pose.theta < 0) or (angle_to_goal >= 0 and self.current_pose.theta >= 0):
                    if self.current_pose.theta > angle_to_goal:
                        vel_msg.angular.z = -0.2
                    else:
                        vel_msg.angular.z = 0.2
                else:
                    if ((pi - abs(angle_to_goal)) + (pi - abs(self.current_pose.theta))) < ((abs(angle_to_goal) - 0) + (abs(self.current_pose.theta) - 0)):
                        if self.current_pose.theta > 0: vel_msg.angular.z = 0.2
                        else: vel_msg.angular.z = -0.2
                    else:
                        if self.current_pose.theta > 0: vel_msg.angular.z = -0.2
                        else: vel_msg.angular.z = 0.2
            else:
                if movement == 0: # west
                    if self.current_pose.y < goal_y: vel_msg.linear.x = 0.2
                    else: m = vel_msg.linear.x = -0.2
                if movement == 1: # north
                    if self.current_pose.x < goal_x: vel_msg.linear.x = 0.2
                    else: m = vel_msg.linear.x = -0.2
                if movement == 2: # east
                    if self.current_pose.y > goal_y: vel_msg.linear.x = 0.2
                    else: m = vel_msg.linear.x = -0.2
                if movement == 3: # south
                    if self.current_pose.x > goal_x: vel_msg.linear.x = 0.2
                    else: vel_msg.linear.x = -0.2
                vel_msg.angular.z = 0.0
            self.velocity_publisher.publish(vel_msg)
            r.sleep()
            current_distance= sqrt(pow((self.current_pose.x - goal_x), 2) + pow((self.current_pose.y - goal_y), 2))
        #After the loop, stops the robot
        vel_msg.angular.z = 0
        vel_msg.linear.x = 0
        self.velocity_publisher.publish(vel_msg)
        rospy.sleep(1)

    def rotateLeft(self):
        print("ROTATE LEFT")
        vel_msg = Twist()
        target = 90
        r = rospy.Rate(4)
        target_rad = pi/2 + (self.rotations*pi)/2
        self.rotations = (self.rotations + 1) % 4
        if target_rad > pi:
            target_rad -= 2*pi
        self.goal_pose.theta = target_rad
        vel_msg.angular.z = 0.2
        #print("target", target_rad, " current ", self.current_pose.theta)
        while abs(target_rad - self.current_pose.theta) > 0.05:
            self.velocity_publisher.publish(vel_msg)    
            #print("target", target_rad, " current ", self.current_pose.theta)
            r.sleep()
        #After the loop, stops the robot
        vel_msg.angular.z = 0
        #Force the robot to stop
        self.velocity_publisher.publish(vel_msg)
        rospy.sleep(1)

    def rotateRight(self):
        print("ROTATE RIGHT")
        vel_msg = Twist()
        target = 90
        r = rospy.Rate(4)
        if self.rotations == 0:
            target_rad = -pi/2
        elif self.rotations == 1:
            target_rad = 0
        elif self.rotations == 2:
            target_rad = pi/2
        elif self.rotations == 3:
            target_rad = pi

        if self.rotations == 0:
            self.rotations = 3
        else:
            self.rotations = self.rotations - 1

        self.goal_pose.theta = target_rad
        vel_msg.angular.z = -0.2
        #print("target", target_rad, " current ", self.current_pose.theta)
        while abs(target_rad - self.current_pose.theta) > 0.05:
            self.velocity_publisher.publish(vel_msg)    
            #print("target", target_rad, " current ", self.current_pose.theta)
            r.sleep()
        #After the loop, stops the robot
        vel_msg.angular.z = 0
        #Force the robot to stop
        self.velocity_publisher.publish(vel_msg)
        rospy.sleep(1)

    def classifyMovement(self, goal_x, goal_y):
        if self.goal_pose.x < goal_x:
            movement = 1 # north
        elif self.goal_pose.x > goal_x:
            movement = 3 # south
        elif self.goal_pose.y > goal_y:
            movement = 2 # east
        elif self.goal_pose.y < goal_y:
            movement = 0 # west
        return movement


