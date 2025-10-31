from math import pi

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class SimulatedLidarPublisher(Node):
    """Publish a rotating synthetic LiDAR scan with configurable noise and angle range."""

    def __init__(self) -> None:
        super().__init__('simulated_lidar_publisher')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('frame_id', 'laser'),
                ('min_angle', -pi),
                ('max_angle', pi),
                ('range_min', 0.05),
                ('range_max', 6.0),
                ('num_readings', 360),
                ('noise_stddev', 0.02),
                ('obstacle_distance', 1.0),
            ],
        )

        period = 1.0 / 15.0
        self.publisher_ = self.create_publisher(LaserScan, 'scan', 10)
        self.timer = self.create_timer(period, self._publish_scan)

    def _publish_scan(self) -> None:
        msg = LaserScan()
        frame_id = self.get_parameter('frame_id').value
        min_angle = float(self.get_parameter('min_angle').value)
        max_angle = float(self.get_parameter('max_angle').value)
        num_readings = int(self.get_parameter('num_readings').value)
        range_min = float(self.get_parameter('range_min').value)
        range_max = float(self.get_parameter('range_max').value)
        noise_stddev = float(self.get_parameter('noise_stddev').value)
        obstacle_distance = float(self.get_parameter('obstacle_distance').value)

        msg.header.frame_id = frame_id
        msg.angle_min = min_angle
        msg.angle_max = max_angle
        msg.angle_increment = (max_angle - min_angle) / max(num_readings - 1, 1)
        msg.time_increment = 0.0
        msg.range_min = range_min
        msg.range_max = range_max

        angles = np.linspace(min_angle, max_angle, num_readings)
        ranges = np.full_like(angles, range_max - 0.5)

        forward_indices = np.logical_and(angles > -0.3, angles < 0.3)
        ranges[forward_indices] = obstacle_distance

        noise = np.random.normal(0.0, noise_stddev, size=num_readings)
        msg.ranges = (ranges + noise).tolist()

        self.publisher_.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = SimulatedLidarPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
