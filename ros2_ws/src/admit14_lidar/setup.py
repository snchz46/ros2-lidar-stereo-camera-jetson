import os
from glob import glob

from setuptools import setup

package_name = 'admit14_lidar'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='Admit14',
    maintainer_email='maintainer@example.com',
    description='LiDAR subscribers and obstacle avoidance demos for Admit 14',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'lidar_simple_listener = admit14_lidar.simple_scan_listener:main',
            'lidar_obstacle_avoidance = admit14_lidar.obstacle_avoidance:main',
            'lidar_turtle_avoidance = admit14_lidar.turtlebot_avoidance:main',
        ],
    },
)
