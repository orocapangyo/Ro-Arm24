# YOLOv8 Setup Guide

Using roboflow website where it helps us to label easily.

---

#### 1. Capture Images with USB Camera

```bash
ffmpeg -f v4l2 -video_size 640x480 -i /dev/video0 -vf fps=1 image_%03d.jpg
```

- This will save one frame per second as `image_001.jpg`, `image_002.jpg`, etc.

#### 2. Upload to Roboflow and Label

1. Go to [https://roboflow.com/](https://roboflow.com/)
2. Create a new dataset project
3. Upload your captured images
4. **Manually label** objects (e.g., red_marker, black_marker, blue_marker)
5. Export the dataset in **YOLOv8 format**

#### 3. Place Dataset in Your Project

```bash
cd ~/ros2_ws/src/yolov8_ros/dataset/
```

Make sure your folder structure looks like:

```
dataset/
├── my_dataset/
│   ├── train/
│   ├── valid/
│   ├── data.yaml
```

#### 4. Train YOLOv8 Model with GPU

```bash
yolo detect train \
  model=yolov8n.pt \
  data=./my_dataset/data.yaml \
  epochs=100 \
  imgsz=640 \
  batch=16
```

#### 5. Run YOLOv8 in ROS 2 with Trained Weights

```bash
ros2 launch yolo_bringup yolov8.launch.py \
  model:=/home/hankyukim/ros2_ws/src/yolov8_ros/dataset/my_dataset/runs/detect/train6/weights/best.pt
```

Make sure you launch the camera node too.

```bash
ros2 launch usb_cam camera.launch.py
```

You may need to adjust yolo bringup launch file to unify image topic name.

🔗 [Roboflow](https://roboflow.com)  
🔗 [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com)
