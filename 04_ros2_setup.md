# ROS 2 Workspace Setup


## Prerequisites  
* ROS 2 Humble (or newer) already installed on the host.  
* Python 3 and *colcon* (comes with most ROS 2 desktop installs).

---

[Complete guide on ros.org/workspace](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)

---

## Ubuntu 22.04

Install extra colcon helpers (optional but handy)
```bash
sudo apt update && sudo apt install -y python3-colcon-common-extensions
```
Create workspace skeleton
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```
Build (even if src is empty, this lays out install/ & build/)
```bash
colcon build --symlink-install
```
Source the workspace for this shell
```bash
source install/setup.bash
```
(Optional) Auto‑source for every new shell
```bash
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

---

## Windows 10 / 11 (PowerShell)

Open a ROS 2 Developer Command Prompt  (or run `ros2` env script manually).
Create workspace
```bash
md C:\ros2_ws\src
cd C:\ros2_ws
```
Build
```bash
colcon build --merge-install
```
Set environment for this session
```bash
.\install\local_setup.ps1  # dot‑source
```
*(For traditional CMD use `install\local_setup.bat` instead.)*

---

## macOS (Apple Silicon & Intel)

Ensure ROS 2 environment is sourced (e.g. via /opt/ros/humble/setup.bash)
Create workspace
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```
Build
```bash
colcon build --symlink-install
```
Source workspace
```bash
source install/setup.bash
```
(Option) add to ~/.zshrc or ~/.bash_profile


---

# How to create ROS2 packages

This guide shows how to turn your stand‑alone Python scripts into a proper ROS 2 package inside a workspace called **`ros2_ws`**. Only valid for Ubuntu 22.04 + ROS 2 Humble and python scripts, other versions not checked.

---

[Complete guide on ros.org/package](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)

---
Create / locate the workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```
Generate a Python package

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_pkg_name
```

* `my_pkg_name` becomes the folder and package name.  
* ROS automatically creates `setup.py`, `package.xml`, and a module folder `my_pkg_name/`.

 Add your scripts

Copy any Python nodes (e.g. `my_script.py`) into the **inner** package folder:

```bash
cp /path/to/my_script.py ~/ros2_ws/src/my_pkg_name/my_pkg_name/
```

Ensure each script:

```python
#!/usr/bin/env python3
# …your imports…

def main():
    # entry‑point code
    pass

if __name__ == "__main__":
    main()
```

Give execute permission (optional but handy):

```bash
chmod +x ~/ros2_ws/src/my_pkg_name/my_pkg_name/my_script.py
```

Expose entry‑points in `setup.py`

Open **`~/ros2_ws/src/my_pkg_name/setup.py`** and locate the `entry_points` block.  Add one line per script:

```python
entry_points={
    'console_scripts': [
        'console_call_name = my_pkg_name.my_script:main',
        # 'another_node = my_pkg_name.another_node:main',
    ],
},
```


Declare dependencies in `package.xml`

Edit **`~/ros2_ws/src/my_pkg_name/package.xml`** and add the runtime deps inside `<exec_depend>` (keep existing ones):

```xml
<exec_depend>import_1</exec_depend>
<exec_depend>import_2</exec_depend>
<exec_depend>import_3</exec_depend>
```

Also keep the default `<buildtool_depend>ament_python</buildtool_depend>`.

Build the workspace

```bash
cd ~/ros2_ws
colcon build --packages-select my_pkg_name --symlink-install
```

* `--symlink-install` allows live editing of Python files without rebuilding.
Source the environment

```bash
# Source ROS 2 installation
source /opt/ros/humble/setup.bash
# Source your freshly built workspace
source ~/ros2_ws/install/setup.bash
```

Add the second line to `~/.bashrc` so it loads automatically:

```bash
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```
Run your package

```bash
ros2 run my_pkg_name console_call_name
```

---

## Admit 14 sample packages

This repository now ships with two ready-to-build ROS 2 Python packages under `ros2_ws/src`:

| Package | Purpose | Handy entry points |
| --- | --- | --- |
| `admit14_camera` | CSI/USB camera publishers and YOLOv8 viewers | `gstreamer_camera_publisher`, `windows_camera_publisher`, `stereo_yolo_viewer`, `windows_yolo_viewer`, `left_eye_yolo_viewer`, `right_eye_yolo_viewer`, `windows_camera_viewer` |
| `admit14_lidar` | LiDAR listeners and simple obstacle avoidance demos | `lidar_simple_listener`, `lidar_obstacle_avoidance`, `lidar_turtle_avoidance` |

Build them with colcon after sourcing your ROS 2 installation:

```bash
cd ~/ros2_ws
colcon build --packages-up-to admit14_camera admit14_lidar --symlink-install
source install/setup.bash
```

### Launching the camera nodes

Start a Jetson CSI camera stream (defaults shown) and override parameters as needed:

```bash
ros2 launch admit14_camera camera_stream.launch.py \
  sensor_id:=0 topic:=/left/image_raw frame_id:=left_camera \
  width:=1280 height:=720 fps:=30
```

To visualise YOLOv8 detections on stereo topics:

```bash
ros2 launch admit14_camera stereo_yolo.launch.py \
  left_topic:=/left/image_raw right_topic:=/right/image_raw \
  model:=yolov8n.pt refresh_hz:=20.0
```

The same executables are also available via `ros2 run admit14_camera …` if you prefer direct command-line use.

### Launching the LiDAR demos

Enable the simple listener by default, or switch on the control loops with launch arguments:

```bash
ros2 launch admit14_lidar lidar_processing.launch.py \
  scan_topic:=/scan obstacle_avoidance:=true \
  dist_threshold:=0.35 linear_speed:=0.25 turn_speed:=0.6
```

To drive the turtlesim example instead, set `turtle_avoidance:=true` and adjust the `turtle_*` parameters.

---

⬅️ [ROS 2 Installation](03_ros2_install.md) | 🔝 [Index](README.md) | ➡️ [Stereo Camera Implementation](05_stereo_cam.md)


