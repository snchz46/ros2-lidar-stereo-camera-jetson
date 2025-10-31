from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    scan_topic = LaunchConfiguration('scan_topic')
    simple_listener = LaunchConfiguration('simple_listener')
    obstacle_avoidance = LaunchConfiguration('obstacle_avoidance')
    turtle_avoidance = LaunchConfiguration('turtle_avoidance')
    cmd_topic = LaunchConfiguration('cmd_topic')
    turtle_cmd_topic = LaunchConfiguration('turtle_cmd_topic')
    dist_threshold = LaunchConfiguration('dist_threshold')
    linear_speed = LaunchConfiguration('linear_speed')
    turn_speed = LaunchConfiguration('turn_speed')
    turtle_forward_speed = LaunchConfiguration('turtle_forward_speed')
    turtle_turn_speed = LaunchConfiguration('turtle_turn_speed')

    return LaunchDescription([
        DeclareLaunchArgument('scan_topic', default_value='/scan'),
        DeclareLaunchArgument('cmd_topic', default_value='/cmd_vel'),
        DeclareLaunchArgument('turtle_cmd_topic', default_value='/turtle1/cmd_vel'),
        DeclareLaunchArgument('dist_threshold', default_value='0.3'),
        DeclareLaunchArgument('linear_speed', default_value='0.2'),
        DeclareLaunchArgument('turn_speed', default_value='0.5'),
        DeclareLaunchArgument('turtle_forward_speed', default_value='2.0'),
        DeclareLaunchArgument('turtle_turn_speed', default_value='1.5'),
        DeclareLaunchArgument('simple_listener', default_value='true'),
        DeclareLaunchArgument('obstacle_avoidance', default_value='false'),
        DeclareLaunchArgument('turtle_avoidance', default_value='false'),
        Node(
            package='admit14_lidar',
            executable='lidar_simple_listener',
            name='lidar_simple_listener',
            condition=IfCondition(simple_listener),
            arguments=['--topic', scan_topic],
        ),
        Node(
            package='admit14_lidar',
            executable='lidar_obstacle_avoidance',
            name='lidar_obstacle_avoidance',
            condition=IfCondition(obstacle_avoidance),
            arguments=[
                '--scan_topic', scan_topic,
                '--cmd_topic', cmd_topic,
                '--dist_threshold', dist_threshold,
                '--linear_speed', linear_speed,
                '--turn_speed', turn_speed,
            ],
        ),
        Node(
            package='admit14_lidar',
            executable='lidar_turtle_avoidance',
            name='lidar_turtle_avoidance',
            condition=IfCondition(turtle_avoidance),
            arguments=[
                '--scan_topic', scan_topic,
                '--cmd_topic', turtle_cmd_topic,
                '--dist_threshold', dist_threshold,
                '--forward_speed', turtle_forward_speed,
                '--turn_speed', turtle_turn_speed,
            ],
        ),
    ])
