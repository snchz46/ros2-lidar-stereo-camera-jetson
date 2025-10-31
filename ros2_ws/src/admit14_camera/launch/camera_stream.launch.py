from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    sensor_id = LaunchConfiguration('sensor_id')
    topic = LaunchConfiguration('topic')
    frame_id = LaunchConfiguration('frame_id')
    width = LaunchConfiguration('width')
    height = LaunchConfiguration('height')
    fps = LaunchConfiguration('fps')

    return LaunchDescription([
        DeclareLaunchArgument('sensor_id', default_value='0'),
        DeclareLaunchArgument('topic', default_value='/camera/image_raw'),
        DeclareLaunchArgument('frame_id', default_value='camera'),
        DeclareLaunchArgument('width', default_value='640'),
        DeclareLaunchArgument('height', default_value='360'),
        DeclareLaunchArgument('fps', default_value='30'),
        Node(
            package='admit14_camera',
            executable='gstreamer_camera_publisher',
            name='csi_camera',
            arguments=[
                '--id', sensor_id,
                '--topic', topic,
                '--frame', frame_id,
                '--width', width,
                '--height', height,
                '--fps', fps,
            ],
        ),
    ])
