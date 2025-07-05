## Ubuntu 22.04에서 ROS2와 YOLOv8 연동 설치 가이드

이 가이드는 Ubuntu 22.04 환경에서 ROS2와 함께 YOLOv8을 설치하고 연동하는 상세한 방법을 안내합니다. ROS2 Humble Hawksbill을 기준으로 설명하며, GPU를 활용한 가속을 위해 NVIDIA 드라이버, CUDA, cuDNN이 사전에 설치되어 있다고 가정합니다.

### 1. 사전 준비: ROS2 및 개발 도구 설치

먼저, ROS2 Humble과 개발에 필요한 도구들이 설치되어 있어야 합니다.

- **ROS2 Humble 설치:** 아직 ROS2를 설치하지 않았다면, 공식 문서를 참고하여 설치를 진행합니다. 일반적으로 다음 명령어를 통해 데스크톱 버전을 설치합니다.
    
    ```bash
    sudo apt update && sudo apt install ros-humble-desktop
    ```
    
- **Colcon 및 개발 도구 설치:** ROS2 패키지 빌드를 위한 `colcon`과 기타 개발 도구들을 설치합니다.
    
    ```bash
    sudo apt install ros-dev-tools
    ```
    

### 2. YOLOv8 ROS2 패키지 설치

YOLOv8을 ROS2와 쉽게 연동하기 위해 공개된 ROS2 패키지를 사용하는 것이 편리합니다. 여기서는 `yolov8_ros` 패키지를 예시로 사용합니다.

- **ROS2 작업 공간 생성:** 패키지를 빌드할 작업 공간(workspace)을 생성합니다.
    
    ```bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws/src
    ```
    
- **`yolov8_ros` 패키지 클론:** GitHub에서 `yolov8_ros` 패키지 소스 코드를 클론합니다.
    
    ```bash
    git clone https://github.com/mgonzs13/yolov8_ros.git
    ```
    
- **의존성 패키지 설치:** `yolov8_ros` 패키지가 필요로 하는 파이썬 라이브러리들을 `requirements.txt` 파일을 이용하여 설치합니다.
    
    ```bash
    cd ~/ros2_ws/src/yolov8_ros
    pip install -r requirements.txt
    ```
    
    > **참고:** `requirements.txt` 파일에는 `ultralytics` (YOLOv8), `torch`, `torchvision` 등 필수 라이브러리들이 포함되어 있습니다.
    > 

### 3. 빌드 및 환경 설정

이제 다운로드한 ROS2 패키지를 빌드하고 실행 환경을 설정합니다.

- **Colcon으로 빌드:** 작업 공간의 최상위 디렉토리로 이동하여 `colcon build` 명령을 실행합니다.
    
    ```bash
    cd ~/ros2_ws
    colcon build
    ```
    
    빌드 과정에서 오류가 발생할 경우, 의존성 패키지가 올바르게 설치되었는지, 시스템에 필요한 라이브러리(예: `python3-opencv`)가 모두 설치되어 있는지 확인하는 것이 좋습니다.
    
- **환경 설정 스크립트 적용:** 빌드가 성공적으로 완료되면, 생성된 설정 파일을 터미널에 적용해야 합니다.
    
    ```bash
    source ~/ros2_ws/install/setup.bash
    ```
    
    매번 새 터미널을 열 때마다 이 명령어를 실행하거나, `~/.bashrc` 파일에 추가하여 자동으로 적용되게 할 수 있습니다.
    
    ```bash
    echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
    source ~/.bashrc
    ```
    

### 4. 실행 및 테스트

모든 설치가 완료되었다면, 웹캠이나 동영상 파일을 이용하여 YOLOv8 ROS2 노드를 실행하고 객체 탐지 결과를 확인할 수 있습니다.

- **카메라 노드 실행 (예시):** 먼저 카메라 영상을 ROS2 토픽으로 게시(publish)하는 노드를 실행해야 합니다. `usb_cam` 패키지나 시스템에 맞는 카메라 드라이버 노드를 사용합니다. `usb_cam` 패키지가 설치되어 있지 않다면 다음 명령어로 설치할 수 있습니다.
    
    ```bash
    sudo apt install ros-humble-usb-cam
    ```
    
    카메라 노드를 실행합니다.
    
    ```bash
    ros2 launch usb_cam camera.launch.py
    ```
    
노트북 카메라를 사용할 때는 usb_cam 패키지의 설정을 조정해야 합니다. 노트북 카메라는 보통 /dev/video0 또는 /dev/video1에 연결되어 있습니다.   
- 노트북 카메라가 /dev/video0에 있다면:
```bash
ros2 launch usb_cam camera.launch.py video_device:=/dev/video0
```

- 노트북 카메라의 성능에 맞게 해상도와 프레임레이트를 조정할 수 있습니다:
```bash
ros2 launch usb_cam camera.launch.py video_device:=/dev/video0 image_width:=640 image_height:=480 framerate:=30
```

- 사용 가능한 비디오 디바이스 확인
```bash
ls /dev/video*
```

- 카메라 정보 확인
```bash
v4l2-ctl --device=/dev/video0 --list-formats-ext
```

- 카메라 권한 문제 해결
```bash
sudo usermod -a -G video $USER
```


- **YOLOv8 노드 실행:** 이제 `yolov8_ros` 패키지의 launch 파일을 실행하여 객체 탐지를 시작합니다. 이 launch 파일은 카메라 토픽을 입력으로 받아 탐지 결과를 이미지와 토픽으로 출력합니다.
    
    ```bash
    ros2 launch yolov8_bringup yolov8.launch.py
    ```
    
    **참고:** 만약 다른 카메라 토픽을 사용한다면, launch 파일의 파라미터를 수정해야 할 수 있습니다. 예를 들어, 입력 이미지 토픽을 변경하려면 다음과 같이 실행합니다.
    
    ```bash
    ros2 launch yolov8_bringup yolov8.launch.py input_image_topic:=/my_camera/image_raw
    ```
    
- **결과 확인:** `rviz2`나 `rqt_image_view`를 사용하여 탐지 결과가 표시된 이미지를 확인할 수 있습니다.
    
    ```bash
    # 탐지 결과 이미지를 rqt_image_view로 확인
    rqt_image_view /yolo/image_raw
    
    # 탐지된 객체 정보를 토픽으로 확인
    ros2 topic echo /yolo/detections
    ```
    

이제 여러분의 ROS2 프로젝트에서 YOLOv8을 활용한 실시간 객체 탐지 기능을 사용할 수 있습니다. 🎉