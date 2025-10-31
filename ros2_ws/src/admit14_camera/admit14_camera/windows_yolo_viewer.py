"""Single camera YOLOv8 viewer for desktop environments."""
from __future__ import annotations

import argparse

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO


class WindowsYoloViewer(Node):
    def __init__(self, topic: str = "/camera/image_raw", model_name: str = "yolov8n.pt") -> None:
        super().__init__("windows_yolo_viewer")
        self._model = YOLO(model_name)
        self._palette = np.random.randint(0, 255, size=(80, 3), dtype=np.uint8)
        self.create_subscription(Image, topic, self._callback, 10)

    def _callback(self, msg: Image) -> None:
        frame = np.frombuffer(msg.data, dtype=np.uint8).reshape(
            msg.height, msg.width, 3
        )
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
        cv2.imshow("Camera + YOLOv8", frame)
        cv2.waitKey(1)

    def destroy_node(self) -> None:  # type: ignore[override]
        cv2.destroyAllWindows()
        super().destroy_node()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', default='/camera/image_raw')
    parser.add_argument('--model', default='yolov8n.pt')
    args, _ = parser.parse_known_args(argv)

    rclpy.init(args=None)
    node = WindowsYoloViewer(topic=args.topic, model_name=args.model)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
