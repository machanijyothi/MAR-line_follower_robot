# Mobile and Autonomous Robots Mini Project

## Jackfruit Problem – Autonomous Robot Navigation using ROS2

## Project Title

Line Following and Obstacle Avoidance

## Overview

This project implements an autonomous mobile robot in a ROS2 and Gazebo simulation environment. The robot navigates on a predefined square track using waypoint-based motion control and odometry feedback.

When an obstacle is detected in front of the robot using LiDAR, the robot switches to obstacle avoidance mode, bypasses the obstacle, and then resumes path following.

This demonstrates core concepts of autonomous robotics such as navigation, sensing, control, and reactive behavior.

---

## Objectives

* Design an autonomous mobile robot in simulation
* Follow a predefined track using waypoints
* Use odometry to estimate robot position
* Detect obstacles using LiDAR
* Avoid obstacles and continue navigation
* Demonstrate ROS2 publisher/subscriber architecture

---

## Features

* Waypoint navigation
* Odometry-based localization
* LiDAR obstacle detection
* Obstacle avoidance state machine
* Gazebo simulation environment
* ROS2 Python controller node

---

## Tools & Technologies

* ROS2
* Gazebo Classic
* Python
* Ubuntu (WSL)
* geometry_msgs/Twist
* nav_msgs/Odometry
* sensor_msgs/LaserScan

---

## Project Structure

```text
line_follower/
├── package.xml
├── setup.py
├── setup.cfg
├── simple_robot.sdf
├── README.md
├── line_follower/
│   ├── __init__.py
│   └── controller.py
└── worlds/
    └── track.world
```

---

## How to Run

### Build Package

```bash
cd ~/mar_ws
colcon build --packages-select line_follower --symlink-install
source install/setup.bash
```

### Launch Gazebo

```bash
gazebo --verbose -s libgazebo_ros_init.so -s libgazebo_ros_factory.so src/line_follower/worlds/track.world

### Spawn Robot

ros2 run gazebo_ros spawn_entity.py -entity simple_bot -file simple_robot.sdf -x 0 -y 6 -z 0.3


### Run Controller

ros2 run line_follower controller

---

## Working Principle

1. Robot starts on the track.
2. Odometry provides current position and orientation.
3. Controller computes angle and distance to next waypoint.
4. Velocity commands are published on `/cmd_vel`.
5. LiDAR continuously checks for obstacles ahead.
6. If obstacle detected:

   * turn left
   * move forward
   * turn right
   * move forward
7. Robot returns to waypoint-following mode.

---

## Output

* Robot successfully follows square path.
* Detects static obstacles.
* Avoids collision.
* Continues autonomous navigation.

---

## Learning Outcomes

* ROS2 nodes and topics
* Publisher/subscriber communication
* Mobile robot control
* Sensor integration
* Gazebo simulation

---

## Team Members

1. Janvi M Shetty
2. Jyothi M
3. Kavana H
4. Karanam Sumedha

---

