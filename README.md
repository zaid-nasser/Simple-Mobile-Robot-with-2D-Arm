# Simple-Mobile-Robot-with-2D-Arm
## Overview
This repository contains a description of a simple differential mobile robot as urdf files. The robot has a 2-DOF revolute manipulator and a camera. Special plugins were implemented to allow the robot to control the robot's and the manipulator's motion. Finally, the potential field algorithm was used to make the robot reach a specified goal by the user. 
## Project structure
- my_robot_description package: this package contains the urdf files defining the robot.
- my_robot_bringup package: this package contains the launch files used in this project. There are three launch files:
  
  1- display.launch.py/.xml: to display the robot using Rviz and check the tfs of the robot.
  
  2- my_robot_gazebo.launch.xml: to view the robot in the Gazebo simulator where you can move it and manipulate the arm using plugins.
  
  3- potential_field_controller.launch.py: to make the robot reach a desired goal inside the Gazebo simulator using the potential field algorithm.
  
- my_robot_control package: this package contains the control algorithm of the robot.

## Installation constructions:
1. Create a workspace and inside the workspace directory Clone this repository.

```
mkdir ~/mobile_robot_proj
cd ~/mobile_robot_proj
git clone https://github.com/ziadnasser98/Simple-mobile-robot-with-2D-manipulator-.git
```
2. Build the workspace using Colcon build in your main directory.

```
cd ~/mobile_robot_proj
colcon build 
```
3. Source the workspace installation file.
```
source install/setup.bash
```
## Running the project
1. To display the robot on Rviz and check the tfs:
   ```
   ros2 launch my_robot_bringup display.launch.xml
   ```
2. To run the robot inside the Gazebo simulator and control the robot and the manipulator, first launch this launch file:
   ```
   ros2 launch my_robot_bringup my_robot_gazebo.launch.xml
   ```
   Then you will see the robot inside the customized world. Open a new terminal and move the robot using the /cmd_vel topic:
   ```
   ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: vel_x}, angular: {z: ang_z}}"
   ```
   To control the arm use this command:
   ```
   ros2 topic pub -1 /set_joint_trajectory trajectory_msgs/msg/JointTrajectory '{header:
   {frame_id: base_footprint}, joint_names: [arm_base_forearm_joint, forearm_hand_joint],
   points: [ {positions: {0.0, 0.0}} ]}'
   ```
3. To make the robot reach a desired goal:

```   
ros2 launch my_robot_bringup potential_field_controller.launch.py goal_x:=4.0 goal_y:=2.0
```
