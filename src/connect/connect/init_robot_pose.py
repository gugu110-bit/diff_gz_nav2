from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy

def main(args=None):
    rclpy.init(args=args)

    navigator = BasicNavigator()

    # 等待导航系统准备就绪
    navigator.waitUntilNav2Active()

    # 设置初始位姿
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.position.z = 0.0
    initial_pose.pose.orientation.x = 0.0
    initial_pose.pose.orientation.y = 0.0
    initial_pose.pose.orientation.z = 0.0
    initial_pose.pose.orientation.w = 1.0

    navigator.setInitialPose(initial_pose)

    #rclpy.spin(navigator)  # Keep the node alive to maintain the initial pose
    rclpy.shutdown()

if __name__ == '__main__':
    main()