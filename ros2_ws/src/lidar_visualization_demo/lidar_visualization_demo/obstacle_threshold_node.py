import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class ObstacleThresholdNode(Node):
    """Log when simulated obstacles breach the configured threshold distance."""

    def __init__(self) -> None:
        super().__init__('obstacle_threshold_node')
        self.declare_parameter('scan_topic', 'scan')
        self.declare_parameter('safety_radius', 0.8)
        self.declare_parameter('warning_radius', 1.2)

        scan_topic = self.get_parameter('scan_topic').get_parameter_value().string_value
        self.safety_radius = float(self.get_parameter('safety_radius').value)
        self.warning_radius = float(self.get_parameter('warning_radius').value)

        self.create_subscription(LaserScan, scan_topic, self._scan_callback, 10)

    def _scan_callback(self, msg: LaserScan) -> None:
        min_range = min(msg.ranges) if msg.ranges else float('inf')
        if min_range < self.safety_radius:
            self.get_logger().warn(f'Obstacle detected at {min_range:.2f} m! Initiating stop.')
        elif min_range < self.warning_radius:
            self.get_logger().info(f'Obstacle approaching: {min_range:.2f} m.')
        else:
            self.get_logger().debug(f'All clear. Closest obstacle {min_range:.2f} m.')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ObstacleThresholdNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
