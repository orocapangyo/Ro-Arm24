import argparse
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from picamera2 import Picamera2, Preview
from libcamera import Transform
import cv2
from cv_bridge import CvBridge

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, 'camera_image', 10)
        self.bridge = CvBridge()  # OpenCV와 ROS2 이미지 메시지 변환기
        self.picam2 = Picamera2()

        # 카메라 설정
        config = self.picam2.create_video_configuration(
            main={"size": (320, 240)},
            transform=Transform(hflip=False, vflip=False)
        )
        self.picam2.configure(config)

        #self.picam2.start_preview(Preview.QT)
        self.picam2.start()

        self.timer = self.create_timer(0.1, self.timer_callback)  # 10Hz로 타이>
        self.get_logger().info("Camera Publisher has started!")

    def timer_callback(self):
        # 카메라에서 한 프레임을 가져와서 ROS2 이미지 메시지로 변환
        frame = self.picam2.capture_array()  # NumPy 배열로 프레임 가져오기

        # 이미지가 4채널일 경우 알파 채널을 제거하여 3채널로 변환
        if frame.shape[2] == 4:  # 4채널(알파 채널 포함)인 경우
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 알파 채널 제거

        # 이미지를 ROS2 이미지 메시지로 변환
        ros_image = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")

        # 이미지를 토픽에 발행
        self.publisher_.publish(ros_image)
        self.get_logger().info("Publishing frame to 'camera_image' topic.")

    def stop_camera(self):
        self.picam2.stop()
        #self.picam2.stop_preview()
        self.picam2.close()
        


def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher()

    try:
        rclpy.spin(camera_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        camera_publisher.stop_camera()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


