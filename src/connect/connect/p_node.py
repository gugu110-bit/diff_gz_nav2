import rclpy
import rclpy.time
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped,Pose
from tf_transformations import euler_from_quaternion,quaternion_from_euler
from nav2_simple_commander.robot_navigator import BasicNavigator
from tf2_ros import Buffer, TransformListener
import sys
from interface.srv import Speech

class PNode(BasicNavigator):
    def __init__(self, node_name='p_node'):
        super().__init__(node_name)
        self.declare_parameter('init_pose', [0.0, 0.0, 0.0])  # 默认初始位姿参数
        self.declare_parameter('target_poses', [-3.0, -2.0, 0.0, 0.0, -5.0, 0.0])  # 默认目标位姿参数
        self.target_poses = self.get_parameter('target_poses').value
        self.init_pose = self.get_parameter('init_pose').value

        self.buffer = Buffer()
        self.tf_listener = TransformListener(self.buffer, self)

        self.client=self.create_client(Speech, 'speak')


    def pose_to_PoseStamped(self,x,y,yaw):
        pose=PoseStamped()
        pose.header.frame_id='map'
        pose.pose.position.x=x
        pose.pose.position.y=y
        pose.pose.position.z=0.0
        q=quaternion_from_euler(0,0,yaw)
        pose.pose.orientation.x=q[0]
        pose.pose.orientation.y=q[1]
        pose.pose.orientation.z=q[2]
        pose.pose.orientation.w=q[3]
        return pose
    
    def set_init_pose(self):
        self.init_pose = self.get_parameter('init_pose').value
        init_pose1=self.pose_to_PoseStamped(self.init_pose[0],self.init_pose[1],self.init_pose[2])
        self.setInitialPose(init_pose1)
        self.waitUntilNav2Active()

    def get_target_poses(self):
        points=[]
        target_poses = self.get_parameter('target_poses').value
        for i in range(0, len(target_poses), 3):
            x = target_poses[i]
            y = target_poses[i + 1]
            yaw = target_poses[i + 2]
            points.append((x, y, yaw))
        return points

    def nav_to_pose(self,target_pose):
        target_pose1=self.pose_to_PoseStamped(target_pose[0],target_pose[1],target_pose[2])
        self.goToPose(target_pose1)
        while not self.isTaskComplete():
            #rclpy.spin_once(self, timeout_sec=0.1)
            status = self.getFeedback()
            if status is not None:
                self.get_logger().info(f'Current navigation status: {status.distance_remaining:.2f} m remaining')
        result = self.getResult()
        self.get_logger().info(f'Navigation result: {result}')

    def get_current_pose(self):
        while rclpy.ok():
            try:
                result=self.buffer.lookup_transform('map', 'base_link', rclpy.time.Time(seconds=0.0),
                    rclpy.time.Duration(seconds=1.0))
                translation = result.transform
                return translation
            except Exception as e:
                self.get_logger().warn(f'Error occurred while looking up transform: {e}')  

    def speak(self,text):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for the speak service...')
        request = Speech.Request()
        request.text = text
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f'语音服务响应: {future.result().success}')
        else:
            self.get_logger().error(f'语音服务响应失败: {future.exception()}')

def main(args=None):
    if args is None:
        args = sys.argv
    rclpy.init(args=args)
    p_node = PNode()
    p_node.speak("正在初始化机器人，请稍候。")
    p_node.set_init_pose()
    p_node.speak("机器人已准备就绪，开始导航。")

    while rclpy.ok():
        target_poses=p_node.get_target_poses()
        for target_pose in target_poses:
            num=target_poses.index(target_pose)+1
            p_node.speak(f"正在前往目标位置 {num}。")
            p_node.nav_to_pose(target_pose)
            p_node.speak(f"已到达目标位置 {num}。")
