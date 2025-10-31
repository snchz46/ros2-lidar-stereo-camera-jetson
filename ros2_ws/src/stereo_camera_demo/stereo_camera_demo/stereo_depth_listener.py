from typing import Optional

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class StereoDepthListener(Node):
    """Listen to the synthetic stereo stream and report simple disparity metrics."""

    def __init__(self) -> None:
        super().__init__('stereo_depth_listener')
        self.declare_parameter('left_topic', 'stereo/left/image_raw')
        self.declare_parameter('right_topic', 'stereo/right/image_raw')
        self.declare_parameter('log_period', 2.0)

        left_topic = self.get_parameter('left_topic').get_parameter_value().string_value
        right_topic = self.get_parameter('right_topic').get_parameter_value().string_value

        self.create_subscription(Image, left_topic, self._handle_left_image, 10)
        self.create_subscription(Image, right_topic, self._handle_right_image, 10)

        self.last_left: Optional[np.ndarray] = None
        self.last_right: Optional[np.ndarray] = None
        self.timer = self.create_timer(self.get_parameter('log_period').value, self._log_disparity)

    def _handle_left_image(self, msg: Image) -> None:
        self.last_left = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)

    def _handle_right_image(self, msg: Image) -> None:
        self.last_right = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)

    def _log_disparity(self) -> None:
        if self.last_left is None or self.last_right is None:
            return
        disparity = np.mean(np.abs(self.last_left.astype(float) - self.last_right.astype(float)))
        self.get_logger().info(f'Average absolute disparity: {disparity:.2f}')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = StereoDepthListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
