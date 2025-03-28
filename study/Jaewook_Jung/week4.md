### 0. 주요 내용

- 라즈베리파이5 환경 구성
- 라즈베리파이5 <-> ESP32 로봇 제어
- YOLOv8 이용해서 물체 인식

### 1. 라즈베리파이5 환경 구성
- 원격 접속을 위해 ssh server 설치
- ROS2 Jazzy 설치

##### 라즈베리파이5 원격 접속 환경 구성하기
```
sudo apt update
sudo apt install openssh-server
```

host(노트북)에서 remote(RPI5)에 접속
```
ssh -X jwj@192.168.0.10
```

##### ROS2 Jazzy 설치

https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html  

위의 공식 문서를 참조해서 설치하면 됨.

colcon build 옵션 자동완성
```
sudo apt install python3-colcon-common-extensions
```

```
echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc
```

##### 노트북과 라즈베리파이 통신
노트북
```
ros2 run demo_nodes_cpp talker
```
RPI5
```
ros2 run demo_nodes_py listener
```

pip3 install (강제 설치)
```
python3 -m pip install -r requirements.txt --break-system-packages
```

##### Humble->Jazzy 버전에 맞게 수정
- .h를 .hpp로 변경
- joint_limits.yaml의 limit: false -> true로 변경, 적절한 값
- 빌드 안되고 필요없는건 빌드 목록에서 제외

### 2. 라즈베리파이5 <-> ESP32 로봇 제어
```
```
```
```