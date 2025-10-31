from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    left_topic = LaunchConfiguration('left_topic')
    right_topic = LaunchConfiguration('right_topic')
    model = LaunchConfiguration('model')
    refresh_hz = LaunchConfiguration('refresh_hz')

    return LaunchDescription([
        DeclareLaunchArgument('left_topic', default_value='/left/image_raw'),
        DeclareLaunchArgument('right_topic', default_value='/right/image_raw'),
        DeclareLaunchArgument('model', default_value='yolov8n.pt'),
        DeclareLaunchArgument('refresh_hz', default_value='30.0'),
        Node(
            package='admit14_camera',
            executable='stereo_yolo_viewer',
            name='stereo_yolo_viewer',
            arguments=[
                '--left_topic', left_topic,
                '--right_topic', right_topic,
                '--model', model,
                '--refresh_hz', refresh_hz,
            ],
        ),
    ])
