from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import rclpy
from tf_transformations import euler_from_quaternion

def main(args=None):
    rclpy.init(args=args)

    navigator = BasicNavigator()

    # 等待导航系统准备就绪
    navigator.waitUntilNav2Active()

    # 设置目标位姿
    target_pose = PoseStamped()
    target_pose.header.frame_id = 'map'
    target_pose.pose.position.x = -3.0
    target_pose.pose.position.y = -2.0
    target_pose.pose.position.z = 0.0
    target_pose.pose.orientation.x = 0.0
    target_pose.pose.orientation.y = 0.0
    target_pose.pose.orientation.z = 0.0
    target_pose.pose.orientation.w = 1.0

    navigator.goToPose(target_pose)

    while not navigator.isTaskComplete():
        status = navigator.getFeedback()
        if status is not None:
            navigator.get_logger().info(f'Current navigation status: {status.current_pose}')
        #rclpy.spin_once(navigator, timeout_sec=0.1)

    #rclpy.spin(navigator)  # Keep the node alive to monitor navigation status
    #rclpy.shutdown()
