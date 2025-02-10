import serial
import argparse
import threading
import time

def read_serial():
    buffer = ""  # 수신 데이터를 저장할 버퍼
    while True:
        if ser.in_waiting > 0:  # 수신된 데이터가 있을 경우
            data = ser.read(ser.in_waiting).decode('utf-8')  # 현재 버퍼에 있는 모든 데이터 읽기
            buffer += data  # 버퍼에 추가
            
            # 메시지의 끝 구분자('\n')를 기준으로 처리
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)  # 첫 번째 메시지와 나머지 분리
                if line.strip():  # 빈 문자열이 아닌 경우 출력
                    print(f"Received: {line.strip()}")

def main():
    global ser
    parser = argparse.ArgumentParser(description='Serial JSON Communication')
    parser.add_argument('port', type=str, help='Serial port name (e.g., COM1 or /dev/ttyUSB0)')

    args = parser.parse_args()

    ser = serial.Serial(args.port, baudrate=115200, timeout=0.1)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    serial_recv_thread = threading.Thread(target=read_serial)
    serial_recv_thread.daemon = True
    serial_recv_thread.start()

    try:
        while True:
            command = input("Input : ")
            ser.write(command.encode() + b'\n')
            time.sleep(0.1)  # Allow time for device response
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()


if __name__ == "__main__":
    main()