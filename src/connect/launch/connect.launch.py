import launch
import launch_ros
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution 


def generate_launch_description():
    p_yaml = PathJoinSubstitution(
        [FindPackageShare('connect'), 'config', 'p_node.yaml']
    )
    
    p_node=Node(
        package='connect',
        executable='p_node',
        name='p_node',
        output='screen',
        parameters=[p_yaml]
    )

    spk_node=Node(
        package='connect',
        executable='speaker',
        name='spk_node',
        output='screen',
    )

    return launch.LaunchDescription([
        p_node,
        spk_node
    ])