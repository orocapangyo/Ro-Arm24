# RoArm Ubuntu 22.04 Virtual Machine Setup Guide

Follow the steps below to set up your RoArm development environment using VMware Player.

---

### 1. Download VMware Player

Go to the following link and download VMware Player:  
👉 [VMware Player Download](https://www.techspot.com/downloads/1969-vmware-player.html)

---

### 2. Install VMware Player

- Extract the downloaded ZIP file.
- Run the installer to install VMware Player.

---

### 3. Download RoArm Ubuntu 22.04 Virtual Machine Image

Download the pre-configured Ubuntu image for RoArm from this link:  
👉 [RoArm VM Download (Google Drive)](https://drive.google.com/drive/folders/1ro-0LlyY9Z8aLXa7fL2Spb7qX5_6lYAP)

---

### 4. Load the VM in VMware Player

- Extract the downloaded ZIP file.
- Launch VMware Player.
- On the right toolbar, click **"Open a Virtual Machine"**.
- Select the `.vmx` file from the extracted `RoArm-M2-S-ROS2-Image` folder.

---

### 5. Start Ubuntu

- Boot into Ubuntu.  
  **Login Password:** `ws`

---

### 6. First-Time Compilation

Open the terminal and run the following:

```bash
cd ~/roarm_ws_em0
sudo chmod +x build_first.sh
. build_first.sh
```

> ⚠️ The initial compilation takes a long time. You can ignore some packages with "stderr output" during this process.

After compilation, you can control the robot arm as shown in the tutorial.

---

### 7. Subsequent Compilation and Use

After making changes to any package, recompile it with:

```bash
cd ~/roarm_ws_em0
. build_common.sh
```

Then, to launch the interactive interface:

```bash
ros2 launch roarm_moveit interact.launch.py
```

---

Happy Developing! 🤖
