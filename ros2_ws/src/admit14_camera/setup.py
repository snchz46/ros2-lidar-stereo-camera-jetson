import os
from glob import glob

from setuptools import setup

package_name = 'admit14_camera'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='Admit14',
    maintainer_email='maintainer@example.com',
    description='Camera publishers and viewers used in the Admit 14 ROS 2 labs',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'gstreamer_camera_publisher = admit14_camera.gstreamer_camera_publisher:main',
            'windows_camera_publisher = admit14_camera.windows_camera_publisher:main',
            'windows_camera_viewer = admit14_camera.windows_camera_viewer:main',
            'windows_yolo_viewer = admit14_camera.windows_yolo_viewer:main',
            'stereo_yolo_viewer = admit14_camera.stereo_yolo_viewer:main',
            'left_eye_yolo_viewer = admit14_camera.mono_yolo_viewers:main_left',
            'right_eye_yolo_viewer = admit14_camera.mono_yolo_viewers:main_right',
        ],
    },
)
