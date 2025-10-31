"""LiDAR based obstacle avoidance examples."""
from __future__ import annotations

import argparse

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class ObstacleAvoidanceNode(Node):
    """Publish velocity commands based on frontal obstacle distance."""

    def __init__(
        self,
        scan_topic: str = "/scan",
        cmd_topic: str = "/cmd_vel",
        dist_threshold: float = 0.3,
        linear_speed: float = 0.2,
        turn_speed: float = 0.5,
    ) -> None:
        super().__init__("obstacle_avoidance_node")

        self._scan_subscription = self.create_subscription(
            LaserScan, scan_topic, self._scan_callback, 10
        )
        self._cmd_publisher = self.create_publisher(Twist, cmd_topic, 10)
        self._latest_scan: LaserScan | None = None
        self._dist_threshold = dist_threshold
        self._linear_speed = linear_speed
        self._turn_speed = turn_speed
        self._timer = self.create_timer(0.5, self._timer_callback)
        self.get_logger().info("Obstacle avoidance node started (2 Hz control).")

    def _scan_callback(self, msg: LaserScan) -> None:
        self._latest_scan = msg

    def _timer_callback(self) -> None:
        if not self._latest_scan or not self._latest_scan.ranges:
            self.get_logger().warn("No valid LiDAR data received.")
            return

        num_points = len(self._latest_scan.ranges)
        center_idx = num_points // 2
        window_size = 10
        start_idx = max(0, center_idx - window_size)
        end_idx = min(num_points, center_idx + window_size)
        frontal_ranges = self._latest_scan.ranges[start_idx:end_idx]
        frontal_ranges = [
            r for r in frontal_ranges if not (r == float("inf") or r != r)
        ]
        if not frontal_ranges:
            self.get_logger().warn("No usable data in frontal LiDAR range.")
            return

        front_dist = min(frontal_ranges)
        twist = Twist()
        if front_dist < self._dist_threshold:
            twist.linear.x = 0.0
            twist.angular.z = self._turn_speed
            self.get_logger().info(
                f"Obstacle detected at {front_dist:.2f} m! Turning."
            )
        else:
            twist.linear.x = self._linear_speed
            twist.angular.z = 0.0
            self.get_logger().info(
                f"Clear path (min: {front_dist:.2f} m). Moving forward."
            )

        self._cmd_publisher.publish(twist)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan_topic', default='/scan')
    parser.add_argument('--cmd_topic', default='/cmd_vel')
    parser.add_argument('--dist_threshold', type=float, default=0.3)
    parser.add_argument('--linear_speed', type=float, default=0.2)
    parser.add_argument('--turn_speed', type=float, default=0.5)
    args, _ = parser.parse_known_args(argv)

    rclpy.init(args=None)
    node = ObstacleAvoidanceNode(
        scan_topic=args.scan_topic,
        cmd_topic=args.cmd_topic,
        dist_threshold=args.dist_threshold,
        linear_speed=args.linear_speed,
        turn_speed=args.turn_speed,
    )
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
