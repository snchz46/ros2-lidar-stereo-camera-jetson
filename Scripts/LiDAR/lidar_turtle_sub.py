#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class TurtleLidarAvoidanceNode(Node):
    def __init__(self):
        super().__init__('turtle_lidar_avoidance_node')

        # Subscribe to LiDAR scan data
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Publish movement commands to the turtlesim turtle
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Store latest scan
        self.latest_scan = None

        # Process scan every half second
        self.timer = self.create_timer(0.5, self.timer_callback)

        self.get_logger().info("Turtle LiDAR avoidance node started.")

    def scan_callback(self, msg):
        # Store the latest scan
        self.latest_scan = msg

    def timer_callback(self):
        if not self.latest_scan or not self.latest_scan.ranges:
            self.get_logger().warn("No valid LiDAR data received.")
            return

        num_points = len(self.latest_scan.ranges)

        # Assume front is around 180° (middle index)
        center_idx = num_points // 2
        window_size = 10
        start_idx = max(0, center_idx - window_size)
        end_idx = min(num_points, center_idx + window_size)

        frontal_ranges = self.latest_scan.ranges[start_idx:end_idx]
        # Remove inf or NaN values
        frontal_ranges = [r for r in frontal_ranges if r != float('inf') and r == r]

        if not frontal_ranges:
            self.get_logger().warn("Frontal scan has no usable data.")
            return

        front_dist = min(frontal_ranges)
        dist_threshold = 0.3  # 30 cm

        twist = Twist()

        if front_dist < dist_threshold:
            # Obstacle ahead: rotate turtle
            twist.linear.x = 0.0
            twist.angular.z = 1.5
            self.get_logger().info(f"Obstacle at {front_dist:.2f} m! Turning.")
        else:
            # Path is clear: move forward
            twist.linear.x = 2.0
            twist.angular.z = 0.0
            self.get_logger().info(f"Clear path ({front_dist:.2f} m). Moving forward.")

        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleLidarAvoidanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
