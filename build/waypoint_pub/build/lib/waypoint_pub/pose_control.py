import rclpy
from rclpy.node import Node
from rclpy.time import Time

import time
import tf2_ros
import numpy as np


class WaypointControl(Node):
    def __init__(self):
        super().__init__("waypoint_pose_controller")

        csv_path = ...

        try:
            self.waypoints = np.loadtxt(csv_path, skiprows=1)
        except:
            self.destroy_node()
            return
        
        self.joint_commands = self.create_publisher(...)    #pose stamped/float64multiarray?

    def run(self)-> None:
        self.get_logger().info("Publishing waypoints...")
        while rclpy.ok() and self.current_index < self.waypoints_to_use.shape[0]-1:
            print("waypoints no",self.waypoints_to_use.shape[0])
            pose_msg, u_msg = self.waypoint_to_msg(self.current_index)

            print("created message, trying to publish")
            self.servo_pub.publish(pose_msg)
            self.u_pub.publish(u_msg)
            self.current_index += 1
            print("published, sleeping")
            time.sleep(3/self.rate_hz)

        self.get_logger().info("Trajectory completed. Reversing in 5 seconds…")
        time.sleep(3)

        for i in reversed(range(self.waypoints_final.shape[0]-1)):
            pose_msg, _ = self.waypoint_to_cmd(i)
            self.servo_pub.publish(pose_msg)
            time.sleep(3/self.rate_hz)

        self.get_logger().info("Execution complete.")
        self.status = "Armed"

    def waypoint_to_cmd(self, index: int) -> Tuple[..., ...]:
        waypoints = self.waypoints_final[index]
        cmdmsg = ...()
        
        return cmdmsg

def main(args=None):
    rclpy.init(args=args)
    node = WaypointControl()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()