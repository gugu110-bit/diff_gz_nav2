from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import rclpy

def main(args=None):
    rclpy.init(args=args)

    navigator = BasicNavigator()

    # 等待导航系统准备就绪
    navigator.waitUntilNav2Active()

    goal_pose=[]

    # 设置目标位姿
    target_pose1 = PoseStamped()
    target_pose1.header.frame_id = 'map'
    target_pose1.pose.position.x = -3.0
    target_pose1.pose.position.y = -2.0
    target_pose1.pose.position.z = 0.0
    target_pose1.pose.orientation.x = 0.0
    target_pose1.pose.orientation.y = 0.0
    target_pose1.pose.orientation.z = 0.0
    target_pose1.pose.orientation.w = 1.0

    target_pose2 = PoseStamped()
    target_pose2.header.frame_id = 'map'
    target_pose2.pose.position.x = 0.0
    target_pose2.pose.position.y = -5.0
    target_pose2.pose.position.z = 0.0
    target_pose2.pose.orientation.x = 0.0
    target_pose2.pose.orientation.y = 0.0
    target_pose2.pose.orientation.z = 0.0
    target_pose2.pose.orientation.w = 1.0

    goal_pose.append(target_pose1)
    goal_pose.append(target_pose2)

    navigator.followWaypoints(goal_pose)

    while not navigator.isTaskComplete():
        status = navigator.getFeedback()
        if status is not None:
            navigator.get_logger().info(f'point_number: {status.current_waypoint}')
    
    result = navigator.getResult()
    navigator.get_logger().info(f'Navigation result: {result}')