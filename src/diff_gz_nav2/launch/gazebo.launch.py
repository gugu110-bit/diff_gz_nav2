import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess,RegisterEventHandler,IncludeLaunchDescription,TimerAction
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit

def generate_launch_description():
    pkg_dir = get_package_share_directory('diff_gz_nav2')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'my_robot.xacro')
    robot_controllers=os.path.join(pkg_dir,'config','my_controllers.yaml')
    
    # 读取 URDF 文件内容作为参数
    robot_description = xacro.process_file(urdf_file).toxml()

    """ # 启动 Gazebo 空世界
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', 'empty.sdf'],
        output='screen'
    ) """
    
    #加载世界文件
    world_file=os.path.join(pkg_dir,'urdf','world2.sdf')
    #world_file='empty.sdf'
    gz_st=PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('ros_gz_sim'), 
                     'launch', 
                     'gz_sim.launch.py'
        )
    )

    gazebo=IncludeLaunchDescription(
        gz_st,
        launch_arguments={
            'gz_args': [f'-r -v 4 ', world_file],
            'on_exit_shutdown': 'true',
            'use_sim_time':'true',
            }.items()
    ) 

    
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 
                     'use_sim_time': True}],  # 确保使用仿真时间
        output='screen'
    )
    
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_robot',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.2',
            '-R', '0.0',
            '-P', '0.0',
            '-Y', '0.0'
        ],
        output='screen',
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster",
                   '--controller-manager', '/controller_manager',
                   '--controller-manager-timeout', '30.0'],
    )
    
    diff_drive_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diffbot_base_controller", 
            "--param-file", robot_controllers,
            "--controller-manager", "/controller_manager", 
            "--controller-manager-timeout", "30.0" ,
            '--ros-args',
            '-r', 'cmd_vel:=/cmd_vel', 
        ],   
    )

    bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=[
        '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        '/lidar_scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
        "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V"
        ],
    remappings=[('/lidar_scan','/scan')],
    output='screen',
    parameters=[{'use_sim_time': True}]
    )

    twist = Node(
        package='connect',
        executable='twist_to_twist_stamped',
        name='twist_converter',
        output='screen',
    )

    
    
    delayed_spawners = TimerAction(
    period=12.0,
    actions=[joint_state_broadcaster_spawner,diff_drive_controller_spawner]
    )
    
    return LaunchDescription([
        gazebo,
        spawn_robot,
        robot_state_publisher,
        delayed_spawners,
        bridge,
        RegisterEventHandler(
            OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[twist],
            )
        ),
    ])
