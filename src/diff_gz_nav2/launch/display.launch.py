from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
import os
import xacro
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 获取包路径
    pkg_dir = get_package_share_directory('diff_gz_nav2')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'my_robot1.urdf')
    
    # 读取 URDF 文件内容作为参数
    with open(urdf_file, 'r') as f:
        robot_description = f.read()
    
    #robot_description = xacro.process_file(urdf_file).toxml()

    # robot_state_publisher 节点
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )
    
    # joint_state_publisher_gui 节点
    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )
    
    # rviz2 节点
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        #arguments=['-d', os.path.join(pkg_dir, 'rviz', 'display.rviz')]  # 可选：保存的 rviz 配置
    )
    
    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz2,
    ])