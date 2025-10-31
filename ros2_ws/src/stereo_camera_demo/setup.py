from setuptools import setup

package_name = 'stereo_camera_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/stereo_preview.launch.py']),
        ('share/' + package_name + '/config', ['config/camera_params.yaml', 'config/rviz_params.yaml']),
        ('share/' + package_name + '/rviz', ['rviz/stereo_preview.rviz']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Samuel Sanchez',
    maintainer_email='samuel.sanchez@example.com',
    description='Demo nodes and launch files for stereo camera previews with RViz.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'stereo_frame_publisher = stereo_camera_demo.stereo_frame_publisher:main',
            'stereo_depth_listener = stereo_camera_demo.stereo_depth_listener:main',
        ],
    },
)
