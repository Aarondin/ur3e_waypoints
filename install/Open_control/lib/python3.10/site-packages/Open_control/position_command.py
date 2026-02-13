import rclpy
from rclpy.node import Node

import numpy as np
from std_msgs.msg import Float64MultiArray

class JointCommands(Node):
    def __init__(self):
        super().__init__("forward_position_commands")

        self.joint_pub = self.create_publisher(Float64MultiArray, '/forward_position_controller/commands', 10)
        self.timer = self.create_timer(0.5, self.command_pub)

    def command_pub(self):

        msg = Float64MultiArray()
        msg.data = np.float64(np.array([]))
        self.joint_pub.publish(msg)