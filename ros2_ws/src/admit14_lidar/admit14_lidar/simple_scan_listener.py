"""Simple LiDAR scan subscribers used throughout the tutorials."""
from __future__ import annotations

import argparse

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class SimpleScanListener(Node):
    """Log the 0th range entry from incoming LaserScan messages."""

    def __init__(self, topic: str = "/scan") -> None:
        super().__init__("rplidar_listener")
        self.create_subscription(LaserScan, topic, self._scan_callback, 10)

    def _scan_callback(self, msg: LaserScan) -> None:
        if msg.ranges:
            self.get_logger().info(f"Distance at angle 0: {msg.ranges[0]:.3f}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', default='/scan')
    args, _ = parser.parse_known_args(argv)

    rclpy.init(args=None)
    node = SimpleScanListener(topic=args.topic)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
