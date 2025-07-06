# RoArm M2-S Full Setup Guide (ROS 2 Humble, USB Cam, YOLOv8)

Follow the steps below to fully set up your RoArm M2-S development environment on Ubuntu with ROS 2 Humble, USB Camera, and YOLOv8.

---

### 1. Install Base Dependencies

```bash
sudo apt update
sudo apt upgrade

sudo apt install git
git clone https://github.com/DUDULRX/roarm_ws_em0.git

sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt upgrade
```

---

### 2. Install ROS 2 Humble and Tools

```bash
sudo apt install ros-humble-desktop
sudo apt install ros-dev-tools
sudo apt install net-tools
sudo apt install ros-humble-moveit-*
sudo apt install ros-humble-foxglove-bridge
sudo apt autoremove ros-humble-moveit-servo-*

echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

### 3. Install Python Requirements and Build RoArm Workspace

```bash
sudo apt install python3-pip

cd ~/roarm_ws_em0
python3 -m pip install -r requirements.txt

cd ~/roarm_ws_em0
sudo chmod +x build_first.sh
. build_first.sh

cd ~/roarm_ws_em0
colcon build

echo "source ~/roarm_ws_em0/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

### 4. Run RoArm Nodes

- **Terminal 1: Run the Driver Node**

```bash
ros2 run roarm_driver roarm_driver
```

- **Terminal 2: Run the Display Node (can be replaced with MoveIt)**

```bash
ros2 launch roarm_description display.launch.py
```

🔗 [RoArm GitHub Repository](https://github.com/waveshareteam/roarm_ws_em0?tab=readme-ov-file)

---

### 5. USB Camera Setup

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/ros-drivers/usb_cam.git
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -y
colcon build
source install/setup.bash
```

To launch the camera node:

```bash
ros2 launch usb_cam camera.launch.py
```

🔗 [USB Cam GitHub Repository](https://github.com/ros-drivers/usb_cam)

---

### 6. YOLOv8 + ROS 2 Setup

```bash
cd ~/ros2_ws/src
git clone https://github.com/mgonzs13/yolov8_ros.git
pip3 install -r yolov8_ros/yolo_ros/requirements.txt

cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

To launch the YOLOv8 node:

```bash
ros2 launch yolo_bringup yolov8.launch.py
```

🔗 [YOLOv8 ROS GitHub Repository](https://github.com/mgonzs13/yolo_ros)
