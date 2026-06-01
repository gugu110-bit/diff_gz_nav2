from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'connect'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name+"/config", ['config/p_node.yaml']),
        ('share/' + package_name+"/launch", glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gugu',
    maintainer_email='gugu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'twist_to_twist_stamped=connect.twist_to_twist_stamped:main',
            'init_robot_pose=connect.init_robot_pose:main',
            'get_robot_pose=connect.get_robot_pose:main',
            'nav_to_pose=connect.nav_to_pose:main',
            'waypoint_follow=connect.waypoint_follow:main',
            'speaker=connect.speaker:main',
            'p_node=connect.p_node:main',
            
        ],
    },
)
