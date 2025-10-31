"""Subscribers that visualise ROS image topics on desktop platforms."""
from __future__ import annotations

import argparse

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class WindowsCameraViewer(Node):
    """Display a single image topic using OpenCV's imshow."""

    def __init__(self, topic: str = "/camera/image_raw") -> None:
        super().__init__("windows_camera_viewer")
        self._subscription = self.create_subscription(
            Image, topic, self._callback, 10
        )

    def _callback(self, msg: Image) -> None:
        frame = np.frombuffer(msg.data, dtype=np.uint8).reshape(
            msg.height, msg.width, 3
        )
        cv2.imshow("Camera", frame)
        cv2.waitKey(1)

    def destroy_node(self) -> None:  # type: ignore[override]
        cv2.destroyAllWindows()
        super().destroy_node()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', default='/camera/image_raw')
    args, _ = parser.parse_known_args(argv)

    rclpy.init(args=None)
    node = WindowsCameraViewer(topic=args.topic)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
