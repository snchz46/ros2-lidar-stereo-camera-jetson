"""Camera publisher nodes for Jetson platforms using GStreamer pipelines."""
from __future__ import annotations

import argparse

import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


PIPE_TPL = (
    "nvarguscamerasrc sensor-id={id} ! "
    "video/x-raw(memory:NVMM),width={width},height={height},framerate={fps}/1 ! "
    "nvvidconv ! video/x-raw,format=BGRx ! "
    "videoconvert ! video/x-raw,format=BGR ! appsink drop=true sync=false"
)


class GStreamerCameraPublisher(Node):
    """Publish frames from a Jetson CSI camera via a GStreamer pipeline."""

    def __init__(
        self,
        sensor_id: int,
        topic: str,
        frame_id: str,
        width: int = 640,
        height: int = 360,
        fps: int = 30,
    ) -> None:
        super().__init__(f"csi_cam_{sensor_id}")
        pipeline = PIPE_TPL.format(id=sensor_id, width=width, height=height, fps=fps)
        self._cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        if not self._cap.isOpened():
            self.get_logger().error(f"Cannot open sensor-id {sensor_id}")
            raise SystemExit(1)

        self._publisher = self.create_publisher(Image, topic, 10)
        self._frame_id = frame_id
        self._timer = self.create_timer(1.0 / float(fps), self._publish_frame)
        self.get_logger().info(
            "Publishing %s from sensor-id %d at %dx%d", topic, sensor_id, width, height
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True, help="sensor-id (0 or 1)")
    parser.add_argument("--topic", type=str, required=True, help="ROS topic to publish")
    parser.add_argument("--frame", type=str, required=True, help="frame_id for the images")
    parser.add_argument("--width", type=int, default=640, help="Frame width")
    parser.add_argument("--height", type=int, default=360, help="Frame height")
    parser.add_argument("--fps", type=int, default=30, help="Publish rate in FPS")
    args, _ = parser.parse_known_args(argv)

    rclpy.init()
    node = GStreamerCameraPublisher(
        sensor_id=args.id,
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
