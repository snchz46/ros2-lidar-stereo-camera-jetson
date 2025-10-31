# Installing ROS2 on Ubuntu 20.04.6 on NVIDIA Jetson Nano

![image](https://github.com/user-attachments/assets/c0bb7570-e373-4814-b670-85ec30277220)

## Quick Navigation

| Section | Jump Link |
| --- | --- |
| Jetson imaging + ROS 2 Foxy | [Go to Jetson instructions](#jetson-nano-with-ubuntu-2004-os-image) |
| Windows 10/11 binary install | [Go to Windows instructions](#ros-2-humble-on-windows-1011) |
| macOS Humble source build | [Go to macOS instructions](#ros-2-humble-on-macos-apple-silicon--intel) |
| Troubleshooting | [Skip to Common Issues](#common-issues) |

## Jetson Nano with Ubuntu 20.04 OS image

[Complete Installation Guide](https://github.com/Qengineering/Jetson-Nano-Ubuntu-20-image?tab=readme-ov-file#installation)

Key tasks from the guide:
- Get a >32 GB SD card to hold the image. 
- Download the image JetsonNanoUb20_3b.img.xz (8.7 GByte!) from [Source](https://ln5.sync.com/dl/403a73c60/bqppm39m-mh4qippt-u5mhyyfi-nnma8c4t/view/default/14418794280004). 
- Flash the image on the SD card with Imager.
- Flash the xz directly, not an unzipped img image. 
- Insert the SD card in your Jetson Nano. 
- Password: jetson

More details on: https://qengineering.eu/install-ubuntu-20.04-on-jetson-nano.html

## ROS2 Foxy Installation
After the successful installation of Ubuntu, open a terminal and time the following commands:

Refresh APT & essential tools

````bash
sudo apt update && sudo apt install curl -y
````
Add ROS 2 GPG key and repository

````bash
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
````
Install desktop variant (∼1 GB)

````bash
sudo apt install ros-foxy-desktop python3-argcomplete

sudo apt install ros-dev-tools
````
Environment setup (auto‑source on every shell)

````bash
echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc
source ~/.bashrc
````
Developer tools

````bash
sudo apt install python3-colcon-common-extensions python3-rosdep

sudo rosdep init
rosdep update
````

---

# ROS 2 Humble on Windows 10/11

Install VS 2022 Build Tools + CMake (if not already).

Follow the official step‑by‑step binary guide → https://docs.ros.org/en/humble/Installation/Windows-Install-Binary.html

After finishing the guide, open x64 Native Tools Command Prompt for VS 2022 and run:

````bash
call "C:\dev\ros2_humble\local_setup.bat"  # adjust to your path
````
Add that call line to a ros2_env.bat file on your desktop so you can double‑click and start a pre‑sourced shell anytime.

Verify:
````bash
ros2 --help
````
If it prints the CLI help, your environment is good to go.

---

# ROS 2 Humble on macOS (Apple Silicon & Intel)

Official doc → https://docs.ros.org/en/humble/Installation/Alternatives/macOS-Development-Setup.html

Cheat‑sheet highlights:

````bash
# Homebrew prereqs
brew install python@3.11 cmake qt @llvm dev tools

# Clone the ros2 repo list & build (takes a while!)
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws
vcs import src < https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos

# Resolve dependencies
rosdep init  # first‑time only (sudo)
rosdep update
rosdep install --from-paths src --ignore-src -y --rosdistro humble

# Build
colcon build --symlink-install

# Source overlay
source install/setup.zsh  # use .bash if you prefer bash
````
Add the source line to your shell RC (.zshrc / .bash_profile) for convenience.

---

## Common Issues

### Jetson Nano

- **APT repository signature errors** – Make sure the system clock is correct (`sudo timedatectl set-ntp true`) before importing the ROS key; re-run the `curl` + `apt update` commands if the key download failed.
- **`rosdep init` permission denied** – Run the command with `sudo` (`sudo rosdep init`) the first time, then `rosdep update` as your regular user.

### Windows 10/11

- **PowerShell execution policy blocks setup** – Run PowerShell as Administrator and execute `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` before sourcing `local_setup.ps1`.
- **`colcon` missing after install** – The binary install does not ship colcon; install it via `python -m pip install -U colcon-common-extensions` inside the ROS command prompt.

### macOS

- **`colcon build` fails due to missing Command Line Tools** – Run `xcode-select --install` once, then retry the build.
- **Python version conflicts** – Ensure the Homebrew Python is first in PATH (`echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile && eval "$(/opt/homebrew/bin/brew shellenv)"`). Re-run `colcon build` after reopening the terminal.

---

⬅️ [ROS 2 Introduction](02_ros2_intro.md) | 🔝 [Index](README.md) | ➡️ [ROS 2 Setup](04_ros2_setup.md)

