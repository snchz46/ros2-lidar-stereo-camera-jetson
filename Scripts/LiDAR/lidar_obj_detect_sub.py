#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')

        # Subscriber to LiDAR (LaserScan) data
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Publisher for velocity commands (Twist)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Variable to store the latest LiDAR scan
        self.latest_scan = None

        # Timer callback to run at 2 Hz (twice per second)
        self.timer = self.create_timer(0.5, self.timer_callback)

        self.get_logger().info("Obstacle avoidance node started (1 Hz control).")

    def scan_callback(self, msg):
        """
        Store the most recent LaserScan message for later processing.
        """
        self.latest_scan = msg

    def timer_callback(self):
        """
        This function runs once per second. It processes the most recent
        LiDAR data and publishes a velocity command based on obstacle distance.
        """
        if not self.latest_scan or not self.latest_scan.ranges:
            self.get_logger().warn("No valid LiDAR data received.")
            return

        # Total number of points in the scan
        num_points = len(self.latest_scan.ranges)

        # Assume the front of the robot is at the middle index
        center_idx = num_points // 2

        # Range window size to check in front of the robot
        window_size = 10
        start_idx = max(0, center_idx - window_size)
        end_idx = min(num_points, center_idx + window_size)

        # Slice the frontal LiDAR data
        frontal_ranges = self.latest_scan.ranges[start_idx:end_idx]

        # Filter out invalid (inf or nan) readings
        frontal_ranges = [r for r in frontal_ranges if not (r == float('inf') or r != r)]

        if not frontal_ranges:
            self.get_logger().warn("No usable data in frontal LiDAR range.")
            return

        # Find the minimum distance to an object in the front sector
        front_dist = min(frontal_ranges)

        # Threshold distance to decide whether to stop or go
        dist_threshold = 0.3  # in meters

        twist = Twist()

        if front_dist < dist_threshold:
            # Obstacle detected: stop and rotate
            twist.linear.x = 0.0
            twist.angular.z = 0.5
            self.get_logger().info(
                f"[2 Hz] Obstacle detected at {front_dist:.2f} m! Turning."
            )
        else:
            # No obstacle: move forward
            twist.linear.x = 0.2
            twist.angular.z = 0.0
            self.get_logger().info(
                f"[2 Hz] Clear path (min: {front_dist:.2f} m). Moving forward."
            )

        # Publish the velocity command
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
