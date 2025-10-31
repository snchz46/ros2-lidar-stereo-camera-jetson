# Implementing LiDAR ROS2 package (only ubuntu)
![image](https://github.com/user-attachments/assets/bb9dfcd6-6884-4252-855d-483c64913795)

Documents, packages and tools: [https://www.slamtec.com/en/Support#rplidar-a-series](https://www.slamtec.com/en/Support#rplidar-a-series)

ROS2 Package [Full guide](https://github.com/Slamtec/rplidar_ros/tree/ros2).

After following the guide above, create a new environment and execute these commands on your Ubuntu terminal:

````bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
````
````bash
git clone -b ros2 https://github.com/Slamtec/rplidar_ros.git
````
````bash
cd ~/ros2_ws/
````
````bash
source /opt/ros/<rosdistro>/setup.bash
````
````bash
colcon build --symlink-install
````
In another terminal run 

````bash
cd ~/ros2_ws/
source ./install/setup.bash
````
Very important command to be able to provide the LiDAR enough power to spin
````bash
sudo chmod 777 /dev/ttyUSB0
````
Package launch command provided by the manufacturer, for our case we need the a2m8 version
````bash
ros2 launch rplidar_ros view_rplidar_a2m8_launch.py
````
After these steps a RViz2 window will appear. Make sure that the topic is set to /scan and the Fixed Frame to "laser"

![Screenshot from 2025-04-13 12-32-52](https://github.com/user-attachments/assets/d55d1b3a-c6bc-4b53-975a-cf20d37777aa)


![Rviz2 LiDAR](https://github.com/user-attachments/assets/fb8bcc4e-8577-458f-adf0-fbe42c887707)


# Retrieving sensor data from the LiDAR

## Script code to read data from the LiDAR

The following Python script demonstrates a minimal ROS 2 node that subscribes to LiDAR data published on the `/scan` topic. It listens for `LaserScan` messages and logs the distance value at angle 0 (the first index of the scan data) as a simple example.

[Minimal LaserScan Publisher](Scripts/LiDAR/lidar_simple_sub.py)

![Screenshot from 2025-04-13 12-33-38](https://github.com/user-attachments/assets/07ff02bc-0f49-4b06-a879-d4ff9a1f7cb6)


## LiDAR-Based Obstacle Avoidance Node

This Python script implements a simple obstacle avoidance node for a robot using LiDAR data in ROS 2.
The node subscribes to the `/scan` topic to receive `LaserScan` messages from the LiDAR sensor and publishes velocity commands to the `/cmd_vel` topic to control the robot's movement.

It analyzes the frontal range of the LiDAR readings, detects obstacles within a specified threshold distance (30 cm), and reacts by either stopping and turning or moving forward if the path is clear.

[obj_detect_lidar.py](Scripts/LiDAR/lidar_obj_detect_sub.py)

https://github.com/user-attachments/assets/6586f72c-890b-40f4-ac10-3be17d219837



![Screenshot from 2025-04-13 12-34-12](https://github.com/user-attachments/assets/057add27-a50d-40a3-aca2-d6dbdd1155c0)

### Implementing LiDAR-Based Obstacle Avoidance Node on Turtlesim

ROS 2 Turtlebot Sim must be running previously on another terminal tab
````bash
ros2 run turtlesim turtlesim_node
````
The Turtlebot controller script publishes Twisting values on the topic /turtle1/cmd_vel based on LiDAR LaserScan data

[Turtlebot LaserScan Controller ](Scripts/LiDAR/lidar_turtle_sub.py)

https://github.com/user-attachments/assets/9bbca0de-e839-4993-8c65-b6a2eeb36290

## ROS 2 Launch Demo (Simulated LiDAR + RViz)

You can test the LiDAR processing pipeline even without hardware by running the new ROS 2 package included in this repository.

```bash
cd ~/ros2_ws
source /opt/ros/<rosdistro>/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch lidar_visualization_demo rviz_lidar.launch.py
```

The launch file will:

- Start `simulated_lidar_publisher`, which streams synthetic `LaserScan` messages according to [`config/lidar_params.yaml`](ros2_ws/src/lidar_visualization_demo/config/lidar_params.yaml).
- Run the `obstacle_threshold_node` listener using [`config/obstacle_detector.yaml`](ros2_ws/src/lidar_visualization_demo/config/obstacle_detector.yaml) so you can adjust warning and stopping distances without editing Python code.
- Open RViz with [`rviz/lidar_viz.rviz`](ros2_ws/src/lidar_visualization_demo/rviz/lidar_viz.rviz). The screenshot below illustrates the expected point cloud ring for the simulated obstacle.

![RViz LiDAR preview](https://github.com/user-attachments/assets/d55d1b3a-c6bc-4b53-975a-cf20d37777aa)

### Recording and Replaying Bags

When hardware is unavailable, record short sessions of the simulated topics to `data/` using:

```bash
ros2 bag record -o data/lidar_demo_bag /scan
```

Replaying those bags with `ros2 bag play data/lidar_demo_bag` allows the visualization and detector nodes to run against consistent data for debugging and regression tests.

---

⬅️ [Stereo Camera Implementation](05_stereo_cam.md) | 🔝 [Index](README.md)
