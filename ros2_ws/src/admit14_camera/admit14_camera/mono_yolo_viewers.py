"""Single-eye YOLO viewers for stereo camera streams."""
from __future__ import annotations

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO


class _BaseEyeViewer(Node):
    def __init__(self, node_name: str, topic: str, window_title: str, model_name: str) -> None:
        super().__init__(node_name)
        self._model = YOLO(model_name)
        self._palette = np.random.randint(0, 255, (80, 3), dtype=np.uint8)
        self._frame: np.ndarray | None = None
        self.create_subscription(Image, topic, self._callback, 10)
        self._timer = self.create_timer(1.0 / 30.0, self._draw)
        self._window_title = window_title

    def _callback(self, msg: Image) -> None:
        frame = np.frombuffer(msg.data, dtype=np.uint8).reshape(
            msg.height, msg.width, 3
        )
        self._frame = frame

    def _annotate(self, frame: np.ndarray) -> np.ndarray:
        result = self._model(frame[..., ::-1], verbose=False)[0]
        for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
            x1, y1, x2, y2 = map(int, box)
            cls_idx = int(cls)
            label = f"{self._model.names[cls_idx]} {conf:.2f}"
            color = tuple(int(v) for v in self._palette[cls_idx])
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
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
        if self._frame is None:
            return
        frame = cv2.flip(self._frame, 1)
        frame = self._annotate(frame)
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow(self._window_title, frame)
        cv2.waitKey(1)

    def destroy_node(self) -> None:  # type: ignore[override]
        cv2.destroyAllWindows()
        super().destroy_node()


class LeftEyeViewer(_BaseEyeViewer):
    def __init__(self, model_name: str = "yolov8n.pt") -> None:
        super().__init__(
            node_name="left_eye_viewer_detect_flip",
            topic="/left/image_raw",
            window_title="Left eye upright + YOLO",
            model_name=model_name,
        )


class RightEyeViewer(_BaseEyeViewer):
    def __init__(self, model_name: str = "yolov8n.pt") -> None:
        super().__init__(
            node_name="right_eye_viewer_detect_flip",
            topic="/right/image_raw",
            window_title="Right eye upright + YOLO",
            model_name=model_name,
        )


def main_left(argv: list[str] | None = None) -> None:
    rclpy.init(args=argv)
    node = LeftEyeViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


def main_right(argv: list[str] | None = None) -> None:
    rclpy.init(args=argv)
    node = RightEyeViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main_left()
