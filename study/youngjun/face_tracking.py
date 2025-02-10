import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from control_msgs.msg import JointJog
from cv_bridge import CvBridge
import cv2
import mediapipe as mp
from rclpy.executors import MultiThreadedExecutor
import time

# MediaPipe 얼굴 인식 모델 초기화
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# 얼굴 감지 모델 로드
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)


class VideoSubscriber(Node):
    def __init__(self, tracking_node):
        super().__init__('video_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera_image',  # 사용하려는 영상 토픽 이름
            self.listener_callback,
            10
        )
        self.bridge = CvBridge()
        self.tracking_node = tracking_node  # Tracking 노드 객체 전달

    def listener_callback(self, msg):
        try:
            # ROS 이미지 메시지를 OpenCV 이미지로 변환
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # 얼굴 감지
            results = face_detection.process(cv_image)

            # 얼굴이 감지되었을 때
            if results.detections:
                for detection in results.detections:
                    # 얼굴 영역의 위치 데이터
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = cv_image.shape

                    # 상대 좌표를 절대 좌표로 변환
                    x1, y1, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                                    int(bboxC.width * iw), int(bboxC.height * ih)

                    # 바운딩 박스 그리기
                    cv2.rectangle(cv_image, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)

                    # 바운딩 박스 중점 계산
                    center_x = x1 + w // 2
                    center_y = y1 + h // 2
                    dx = 160 - center_x
                    dy = 120 - center_y

                    # 중점 좌표 출력
                    #print(f"Center: ({center_x}, {center_y})")
                    
                    # Tracking 노드로 이동 명령 전달
                    self.tracking_node.move(dx, dy)

            # 얼굴 인식 결과를 OpenCV 창에 표시
            #cv2.imshow("Video Feed", cv_image)
            #cv2.waitKey(1)  # 1ms 대기 후 키 입력을 대기 (GUI 업데이트)

        except Exception as e:
            self.get_logger().error(f'Error converting image: {e}')

class Tracking(Node):
    def __init__(self):
        super().__init__('joint_command_publisher')
        self.publisher_ = self.create_publisher(JointJog, '/servo_node/delta_joint_cmds', 10)

        self.x_error = 40 #크기가 작을수록 정확성 상승
        self.y_error = 20 #크기가 작을수록 정확성 상승
        self.const_Vx = 0.02 #속도 상수 클수록 속도 상승
        self.const_Vy = 0.03 #속도 상수 클수록 속도 상승
        self.minimum_Vx = 0.6 #x축 최소 속도
        self.minimum_Vy = 0.6 #y축 최소 속도
        self.dx_stabillity = True #x축 안정 판별
        self.dy_stabillity = True #y축 안정 판별

    def move(self, dx, dy):
        msg = JointJog()
        
        # 예시: x 방향으로만 조정
        if abs(dx) > self.x_error:
            if dx >= self.x_error:
                self.dx_stabillity = False
                # header 생성
                msg.header.stamp.sec = int(time.time())
                msg.header.stamp.nanosec = int((time.time() - int(time.time())) * 10 ** 9)
                msg.header.frame_id = 'base_link'

                # joint_names
                msg.joint_names = ['base_link_to_link1']

                # displacements (혹은 position_deltas)
                # msg.displacements = [0.5, 1.0]

                # velocities
                v = -self.const_Vx * dx
                if abs(v) < self.minimum_Vx:
                    v = self.minimum_Vx
                msg.velocities = [v]  # x 방향으로 속도 조정

                # Publish joint jog message
                self.publisher_.publish(msg)
                #self.get_logger().info(f'Published joint command: {msg.velocities}')
            elif dx <= -self.x_error:
                self.dx_stabillity = False
                # header 생성
                msg.header.stamp.sec = int(time.time())
                msg.header.stamp.nanosec = int((time.time() - int(time.time())) * 10 ** 9)
                msg.header.frame_id = 'base_link'

                # joint_names
                msg.joint_names = ['base_link_to_link1']

                # displacements (혹은 position_deltas)
                # msg.displacements = [0.5, 1.0]

                # velocities
                v = -self.const_Vx * dx
                if abs(v) < self.minimum_Vx:
                    v = self.minimum_Vx
                msg.velocities = [v]  # x 방향으로 속도 조정

                # Publish joint jog message
                self.publisher_.publish(msg)
                #self.get_logger().info(f'Published joint command: {msg.velocities}')
        else:
            self.dx_stabillity = True
        
        if self.dx_stabillity == True:
            if dy >= self.y_error:
                self.dy_stabillity = False
                # header 생성
                msg.header.stamp.sec = int(time.time())
                msg.header.stamp.nanosec = int((time.time() - int(time.time())) * 10 ** 9)
                msg.header.frame_id = 'base_link'

                # joint_names
                msg.joint_names = ['link2_to_link3']

                # displacements (혹은 position_deltas)
                # msg.displacements = [0.5, 1.0]

                # velocities
                v = -self.const_Vy * dy
                if abs(v) < self.minimum_Vy:
                    v = self.minimum_Vy
                msg.velocities = [v]  # y 방향으로 속도 조정

                # Publish joint jog message
                self.publisher_.publish(msg)
                #self.get_logger().info(f'Published joint command: {msg.velocities}')
            elif dy <= -self.y_error:
                self.dy_stabillity = False
                # header 생성
                msg.header.stamp.sec = int(time.time())
                msg.header.stamp.nanosec = int((time.time() - int(time.time())) * 10 ** 9)
                msg.header.frame_id = 'base_link'

                # joint_names
                msg.joint_names = ['link2_to_link3']

                # displacements (혹은 position_deltas)
                # msg.displacements = [0.5, 1.0]

                # velocities
                v = -self.const_Vy * dy
                if abs(v) < self.minimum_Vy:
                    v = self.minimum_Vy
                msg.velocities = [v]  # y 방향으로 속도 조정

                # Publish joint jog message
                self.publisher_.publish(msg)
                #self.get_logger().info(f'Published joint command: {msg.velocities}')
            else:
                self.dy_stabillity = True

        if self.dx_stabillity == True and self.dy_stabillity == True:
            print('\r안정    ', end='', flush=True)
        else:
            print('\r화면 조정', end='', flush=True)
            

def main(args=None):
    rclpy.init(args=args)

    # Tracking 노드 인스턴스 생성
    tracking_node = Tracking()

    # VideoSubscriber 노드에 Tracking 노드 전달
    video_subscriber_node = VideoSubscriber(tracking_node)

    executor = MultiThreadedExecutor()
    executor.add_node(video_subscriber_node)
    executor.add_node(tracking_node)

    try:
        # 멀티쓰레드를 활용해 노드 실행
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        video_subscriber_node.destroy_node()
        tracking_node.destroy_node()
        rclpy.shutdown()

    # 종료 시 자원 해제
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

