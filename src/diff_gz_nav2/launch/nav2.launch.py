import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
   
    pkg_name = 'diff_gz_nav2'

    map_file = LaunchConfiguration(
        'map',
        default=os.path.join(
            get_package_share_directory(pkg_name),
            'map',
            'my_map.yaml'
        )
    )

    params_file = LaunchConfiguration(
        'params_file',
        default=os.path.join(
            get_package_share_directory(pkg_name),
            'config',
            'nav2_params.yaml'
        )
    )

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    rviz_launch_cmd = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=[
            '-d', os.path.join(get_package_share_directory(pkg_name), 'rviz', 'nav2_default_view.rviz')
        ]
    )

 
    # 自动启动 map_server、AMCL、规划器、控制器、行为树等节点
    nav2_bringup1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('nav2_bringup'),
                'launch',
                'localization_launch.py'
            )
        ),
        launch_arguments={
            'map': map_file,
            'params_file': params_file,
            'use_sim_time': use_sim_time,
        }.items()
    )
    nav2_bringup2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('nav2_bringup'),
                'launch',
                'navigation_launch.py'
            )
        ),
        launch_arguments={
            'params_file': params_file,
            'use_sim_time': use_sim_time,
        }.items()
    )


    return LaunchDescription([

        nav2_bringup1,
        nav2_bringup2,
        rviz_launch_cmd,
    ])