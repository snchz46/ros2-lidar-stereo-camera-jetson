from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterFile


def generate_launch_description():
    package_dir = Path(get_package_share_directory('stereo_camera_demo'))

    default_params = package_dir / 'config' / 'camera_params.yaml'
    listener_params = package_dir / 'config' / 'rviz_params.yaml'
    rviz_config = package_dir / 'rviz' / 'stereo_preview.rviz'

    params_arg = DeclareLaunchArgument(
        'camera_params',
        default_value=str(default_params),
        description='YAML file with stereo camera parameters.',
    )
    listener_params_arg = DeclareLaunchArgument(
        'listener_params',
        default_value=str(listener_params),
        description='YAML file configuring the stereo depth listener.',
    )

    stereo_publisher = Node(
        package='stereo_camera_demo',
        executable='stereo_frame_publisher',
        name='stereo_frame_publisher',
        parameters=[ParameterFile(LaunchConfiguration('camera_params'), allow_substs=True)],
        output='screen',
    )

    disparity_logger = Node(
        package='stereo_camera_demo',
        executable='stereo_depth_listener',
        name='stereo_depth_listener',
        parameters=[ParameterFile(LaunchConfiguration('listener_params'), allow_substs=True)],
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='stereo_rviz',
        arguments=['-d', str(rviz_config)],
        output='screen',
    )

    return LaunchDescription([
        params_arg,
        listener_params_arg,
        stereo_publisher,
        disparity_logger,
        rviz,
    ])
