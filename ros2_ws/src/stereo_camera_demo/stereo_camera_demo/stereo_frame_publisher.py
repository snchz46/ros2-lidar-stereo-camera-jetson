from typing import Tuple

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image


class StereoFramePublisher(Node):
    """Publish synthetic stereo images so that RViz and subscribers have data."""

    def __init__(self) -> None:
        super().__init__('stereo_frame_publisher')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('frame_id', 'stereo_camera'),
                ('width', 640),
                ('height', 480),
                ('baseline_m', 0.06),
                ('focal_length_px', 320.0),
                ('publish_rate_hz', 5.0),
                ('gradient_direction', 'horizontal'),
            ],
        )

        publish_rate = float(self.get_parameter('publish_rate_hz').value)
        self.publish_period = 1.0 / max(publish_rate, 0.1)

        self.left_image_pub = self.create_publisher(Image, 'stereo/left/image_raw', 10)
        self.right_image_pub = self.create_publisher(Image, 'stereo/right/image_raw', 10)
        self.left_info_pub = self.create_publisher(CameraInfo, 'stereo/left/camera_info', 10)
        self.right_info_pub = self.create_publisher(CameraInfo, 'stereo/right/camera_info', 10)

        self.timer = self.create_timer(self.publish_period, self.publish_images)
        self.get_logger().info('Stereo frame publisher ready.')

    def publish_images(self) -> None:
        width = int(self.get_parameter('width').value)
        height = int(self.get_parameter('height').value)
        frame_id = str(self.get_parameter('frame_id').value)
        gradient_direction = str(self.get_parameter('gradient_direction').value).lower()

        left_image, right_image = self._generate_stereo_pair(width, height, gradient_direction)
        left_msg = self._to_image_msg(left_image, frame_id + '_left')
        right_msg = self._to_image_msg(right_image, frame_id + '_right')

        cam_info_left = self._camera_info(width, height, frame_id + '_left')
        cam_info_right = self._camera_info(width, height, frame_id + '_right')

        self.left_image_pub.publish(left_msg)
        self.right_image_pub.publish(right_msg)
        self.left_info_pub.publish(cam_info_left)
        self.right_info_pub.publish(cam_info_right)

    def _generate_stereo_pair(self, width: int, height: int, gradient_direction: str) -> Tuple[np.ndarray, np.ndarray]:
        ramp = np.linspace(0, 255, num=width if gradient_direction == 'horizontal' else height, dtype=np.uint8)
        if gradient_direction == 'horizontal':
            base_image = np.tile(ramp, (height, 1))
        else:
            base_image = np.tile(ramp[:, np.newaxis], (1, width))
        base_image = np.stack([base_image] * 3, axis=-1)

        disparity_shift = 5
        right_image = np.roll(base_image, shift=disparity_shift, axis=1)
        return base_image, right_image

    def _to_image_msg(self, image: np.ndarray, frame_id: str) -> Image:
        msg = Image()
        msg.header.frame_id = frame_id
        msg.height, msg.width, _ = image.shape
        msg.encoding = 'rgb8'
        msg.step = msg.width * 3
        msg.data = image.tobytes()
        return msg

    def _camera_info(self, width: int, height: int, frame_id: str) -> CameraInfo:
        baseline = float(self.get_parameter('baseline_m').value)
        focal_length = float(self.get_parameter('focal_length_px').value)
        msg = CameraInfo()
        msg.header.frame_id = frame_id
        msg.width = width
        msg.height = height
        msg.k = [focal_length, 0.0, width / 2.0, 0.0, focal_length, height / 2.0, 0.0, 0.0, 1.0]
        msg.p = [focal_length, 0.0, width / 2.0, 0.0, 0.0, focal_length, height / 2.0, 0.0, 0.0, 0.0, 1.0, -focal_length * baseline]
        return msg


def main(args=None) -> None:
    rclpy.init(args=args)
    node = StereoFramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
