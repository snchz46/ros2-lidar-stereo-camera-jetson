# Abstract
Robot Operating System 2 (ROS2) is an open-source middleware framework for developing distributed and modular robotic applications. It has native support for real-time communication, cross-platform compatibility, and easy interfacing with packages like Simulink and MATLAB.

This renders it a perfect middleware for prototyping and deployment of autonomous features in both academic and industrial environments. This research covers the integration and implementation of ROS2 nodes for fusing LiDAR and stereo camera sensors on a Jetson Orin Nano controller. 

The theoretical foundation underlying this project is part of a broader research project named Automated Driving in Miniaturized Traffic scenarios 1:14 (ADMIT14), which are intended to validate autonomous driving technology in a controlled, small-scale environment. In this study, we concentrate on creating a modular configuration, where Python Publishers transmit raw sensor data, and Python subscribers or MATLAB decode them at higher levels. This isolated configuration allows independent development, testing, and replacement of individual hardware components, showcasing the versatility that ROS2 provides.

# Introduction

Autonomous driving technologies essentially rely on the integration of various sensors and control components to perceive, interpret, and react to their environment. In complex systems such as autonomous cars, it is necessary to ensure that every subsystem can be developed, tested, and updated independently, which is crucial for scaling up and for the sake of long-term sustainability.

The ADMIT14 program, Automated Driving in Miniaturized Traffic environments scale 1:14, was started at Hochschule Esslingen with the vision of validating and testing autonomous functionality in a manageable miniature environment. Our work within this paradigm revolves around the realization of a sensor fusion architecture with ROS2, by means of LiDAR technology and stereo cameras on an NVIDIA Jetson platform.

# Proposed System Architecture

## Logical Architecture

Image shows the modular framework employed in this project. The system architecture is divided into two areas. On the left side, in the blue area, the Jetson ROS2 setup takes care of the management of data from the RPLIDAR and Stereo Camera. The RPLIDAR and Stereo Camera are each interfaced with specific Python-based ROS2 nodes that publish sensor data on the following topics: \texttt{/scan}, \texttt{/raw\_image\_left}, and \texttt{/raw\_image\_right}. 

Then, the Jetson executes a series of ROS2 nodes that receive the sensor data published by the sensor nodes and then publish appropriate control commands through a CAN interface. The interface serves to connect the ROS2 system to an external Arduino microcontroller. 

In the right side of the architecture, red area, the Arduino processes incoming CAN messages and transmits commands to the respective actuators. This divided arrangement enables each hardware unit to be developed, tested, and replaced independently, thereby illustrating the flexibility fostered by ROS2 in modular architectures.

![system arch](https://github.com/user-attachments/assets/f654b3a4-083b-4bbb-9059-a9da8de3f44a)

## Physical Architecture

![system arch HW](https://github.com/user-attachments/assets/ff30c387-1821-4c4f-a1b8-d86c69059528)

---

🔝 [Index](README.md) | ➡️ [ROS 2 Introduction](02_ros2_intro.md)
