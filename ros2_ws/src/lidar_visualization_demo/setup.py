from setuptools import setup

package_name = 'lidar_visualization_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/rviz_lidar.launch.py']),
        ('share/' + package_name + '/config', ['config/lidar_params.yaml', 'config/obstacle_detector.yaml']),
        ('share/' + package_name + '/rviz', ['rviz/lidar_viz.rviz']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Samuel Sanchez',
    maintainer_email='samuel.sanchez@example.com',
    description='Simulated LiDAR nodes and RViz visualization launch file.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simulated_lidar_publisher = lidar_visualization_demo.simulated_lidar_publisher:main',
            'obstacle_threshold_node = lidar_visualization_demo.obstacle_threshold_node:main',
        ],
    },
)
