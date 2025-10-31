from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterFile


def generate_launch_description():
    package_dir = Path(get_package_share_directory('lidar_visualization_demo'))

    default_lidar_params = package_dir / 'config' / 'lidar_params.yaml'
    default_detector_params = package_dir / 'config' / 'obstacle_detector.yaml'
    rviz_config = package_dir / 'rviz' / 'lidar_viz.rviz'

    lidar_params_arg = DeclareLaunchArgument(
        'lidar_params',
        default_value=str(default_lidar_params),
        description='LiDAR publisher parameter file.',
    )
    detector_params_arg = DeclareLaunchArgument(
        'detector_params',
        default_value=str(default_detector_params),
        description='Obstacle detector parameter file.',
    )

    lidar_publisher = Node(
        package='lidar_visualization_demo',
        executable='simulated_lidar_publisher',
        name='simulated_lidar_publisher',
        parameters=[ParameterFile(LaunchConfiguration('lidar_params'), allow_substs=True)],
        output='screen',
    )

    obstacle_detector = Node(
        package='lidar_visualization_demo',
        executable='obstacle_threshold_node',
        name='obstacle_threshold_node',
        parameters=[ParameterFile(LaunchConfiguration('detector_params'), allow_substs=True)],
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='lidar_rviz',
        arguments=['-d', str(rviz_config)],
        output='screen',
    )

    return LaunchDescription([
        lidar_params_arg,
        detector_params_arg,
        lidar_publisher,
        obstacle_detector,
        rviz,
    ])
