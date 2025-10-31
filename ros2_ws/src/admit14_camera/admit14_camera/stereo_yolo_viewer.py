"""Stereo camera visualisation with YOLOv8 annotations."""
from __future__ import annotations

import argparse

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO


class StereoYoloViewer(Node):
    """Subscribe to left/right camera topics and display YOLOv8 detections."""

    def __init__(
        self,
        left_topic: str = "/left/image_raw",
        right_topic: str = "/right/image_raw",
        model_name: str = "yolov8n.pt",
        refresh_hz: float = 30.0,
    ) -> None:
        super().__init__("stereo_yolo_viewer")

        self._left_image: np.ndarray | None = None
        self._right_image: np.ndarray | None = None

        self.create_subscription(Image, left_topic, self._left_cb, 10)
        self.create_subscription(Image, right_topic, self._right_cb, 10)

        self._model = YOLO(model_name)
        self._palette = np.random.randint(0, 255, size=(80, 3), dtype=np.uint8)
        self._timer = self.create_timer(1.0 / refresh_hz, self._draw)

    def _left_cb(self, msg: Image) -> None:
        self._left_image = self._msg_to_cv(msg)

    def _right_cb(self, msg: Image) -> None:
        self._right_image = self._msg_to_cv(msg)

    @staticmethod
    def _msg_to_cv(msg: Image) -> np.ndarray:
        image = np.frombuffer(msg.data, dtype=np.uint8)
        return image.reshape(msg.height, msg.width, 3)

    def _annotate(self, frame: np.ndarray) -> np.ndarray:
        result = self._model(frame[..., ::-1], verbose=False)[0]
        for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
            x1, y1, x2, y2 = map(int, box)
            cls_idx = int(cls)
            label = f"{self._model.names[cls_idx]} {conf:.2f}"
            color = tuple(int(v) for v in self._palette[cls_idx])

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            (tw, th), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )
            cv2.rectangle(frame, (x1, y1 - th - 4), (x1 + tw, y1), color, -1)
            cv2.putText(
                frame,
                label,
                (x1, y1 - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
        return frame

    def _draw(self) -> None:
        if self._left_image is None or self._right_image is None:
            return

        height = min(self._left_image.shape[0], self._right_image.shape[0])
        width = min(self._left_image.shape[1], self._right_image.shape[1])
        left = cv2.flip(self._left_image[:height, :width], 0)
        right = cv2.flip(self._right_image[:height, :width], 0)

        left = self._annotate(left)
        right = self._annotate(right)

        cv2.imshow("Stereo + YOLO", np.hstack((left, right)))
        cv2.waitKey(1)

    def destroy_node(self) -> None:  # type: ignore[override]
        cv2.destroyAllWindows()
        super().destroy_node()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--left_topic', default='/left/image_raw')
    parser.add_argument('--right_topic', default='/right/image_raw')
    parser.add_argument('--model', default='yolov8n.pt')
    parser.add_argument('--refresh_hz', type=float, default=30.0)
    args, _ = parser.parse_known_args(argv)

    rclpy.init(args=None)
    node = StereoYoloViewer(
        left_topic=args.left_topic,
        right_topic=args.right_topic,
        model_name=args.model,
        refresh_hz=args.refresh_hz,
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
