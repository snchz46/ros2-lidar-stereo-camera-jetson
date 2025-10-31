"""Camera publisher nodes for USB webcams on Windows."""
from __future__ import annotations

import argparse

import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class WindowsCameraPublisher(Node):
    """Publish frames from a USB webcam using the DirectShow backend."""

    def __init__(
        self,
        device_index: int,
        topic: str,
        frame_id: str,
        width: int = 1280,
        height: int = 720,
        fps: int = 30,
    ) -> None:
        super().__init__(f"win_cam_{device_index}")

        self._cap = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)
        if not self._cap.isOpened():
            self.get_logger().error(f"No camera detected {device_index}")
            raise SystemExit(1)

        if width and height:
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(width))
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(height))

        self._publisher = self.create_publisher(Image, topic, 10)
        self._frame_id = frame_id
        self._timer = self.create_timer(1.0 / float(fps), self._publish_frame)
        self.get_logger().info(
            "Publishing %s from camera device %d at %dx%d",
            topic,
            device_index,
            width,
            height,
        )

    def _publish_frame(self) -> None:
        ok, frame = self._cap.read()
        if not ok:
            self.get_logger().warning("Frame lost")
            return

        msg = Image()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self._frame_id
        msg.height, msg.width = frame.shape[:2]
        msg.encoding = "bgr8"
        msg.step = msg.width * 3
        msg.data = frame.tobytes()
        self._publisher.publish(msg)

    def destroy_node(self) -> None:  # type: ignore[override]
        if self._cap.isOpened():
            self._cap.release()
        super().destroy_node()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Publish a Windows webcam to ROS 2")
    parser.add_argument("--id", type=int, default=0, help="Device index (0 = first webcam)")
    parser.add_argument("--topic", type=str, default="/camera/image_raw", help="ROS topic")
    parser.add_argument("--frame", type=str, default="webcam", help="TF frame_id")
    parser.add_argument("--width", type=int, default=1280, help="Frame width")
    parser.add_argument("--height", type=int, default=720, help="Frame height")
    parser.add_argument("--fps", type=int, default=30, help="Publish rate in FPS")
    args, _ = parser.parse_known_args(argv)

    rclpy.init()
    node = WindowsCameraPublisher(
        device_index=args.id,
        topic=args.topic,
        frame_id=args.frame,
        width=args.width,
        height=args.height,
        fps=args.fps,
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
