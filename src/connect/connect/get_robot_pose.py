"""Get robot pose in the map frame by listening to AMCL TF.

This node listens for the TF published by AMCL (typically a transform
from `map` -> `base_link`) and returns the robot pose (x, y, yaw).

Usage: run the file as a script or import `GetRobotPose` and call
`get_pose()` from an rclpy context.
"""

import math
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from tf_transformations import euler_from_quaternion

from tf2_ros import Buffer, TransformListener

class GetRobotPose(Node):
    def __init__(self):
        super().__init__('get_robot_pose')
        self.buffer = Buffer()
        self.tf_listener = TransformListener(self.buffer, self)
        self.timer = self.create_timer(1.0, self.get_pose) 

    def get_pose(self, timeout_sec=5.0):
        try:
            now = rclpy.time.Time()
            self.buffer.can_transform('map', 'base_link', now, timeout=Duration(seconds=timeout_sec))
            transform = self.buffer.lookup_transform('map', 'base_link', now)
            x = transform.transform.translation.x
            y = transform.transform.translation.y
            q = transform.transform.rotation
            _, _, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
            self.get_logger().info(f'Robot pose: x={x:.2f}, y={y:.2f}, yaw={math.degrees(yaw):.1f} degrees')
            return x, y, yaw
        except Exception as e:
            self.get_logger().error(f'Failed to get robot pose: {e}')
            return None
        
def main(args=None):
    rclpy.init(args=args)
    node = GetRobotPose()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':    main()
 
