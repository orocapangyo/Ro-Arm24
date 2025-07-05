# YOLOv8 커스텀 모델 학습 가이드

이 문서는 YOLOv8을 활용하여 자신만의 데이터셋으로 커스텀 객체 탐지 모델을 학습하는 방법을 단계별로 안내합니다.

---

## 1. 환경 준비

- **Python 3.8 이상**이 필요합니다.
- **필수 패키지 설치:**

```bash
pip install ultralytics
```

- (선택) GPU 사용 시, CUDA 및 cuDNN이 설치되어 있어야 합니다.

---

## 2. 데이터셋 준비

YOLOv8은 YOLO 포맷의 데이터셋을 사용합니다.

### 2.1 디렉토리 구조 예시

```
my_dataset/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```

- `images/train/`, `images/val/`: 학습/검증 이미지
- `labels/train/`, `labels/val/`: 각 이미지와 동일한 이름의 `.txt` 파일 (YOLO 라벨 포맷)
- `data.yaml`: 데이터셋 구성 파일

### 2.2 라벨 포맷
- 각 줄: `<class_id> <x_center> <y_center> <width> <height>` (값은 0~1 사이, 상대좌표)

### 2.3 data.yaml 예시
```yaml
train: ./images/train
val: ./images/val
nc: 2  # 클래스 개수
names: ['class1', 'class2']
```

---

## 3. 커스텀 학습 설정

- 사전학습된 모델(예: yolov8n.pt, yolov8s.pt 등)을 사용할 수 있습니다.
- 하이퍼파라미터는 기본값을 사용하거나 필요에 따라 조정합니다.

---

## 4. 학습 실행

```bash
yolo detect train \
  model=yolov8n.pt \
  data=./my_dataset/data.yaml \
  epochs=100 \
  imgsz=640 \
  batch=16
```

- `model`: 사용할 사전학습 모델
- `data`: 데이터셋 yaml 파일 경로
- `epochs`: 학습 반복 횟수
- `imgsz`: 입력 이미지 크기
- `batch`: 배치 크기

---

## 5. 학습 결과 확인 및 추론

- 학습 결과는 `runs/detect/train` 폴더에 저장됩니다.
- 최적의 가중치 파일: `runs/detect/train/weights/best.pt`

### 5.1 추론 예시
```bash
yolo detect predict \
  model=runs/detect/train/weights/best.pt \
  source=path/to/test/images
```

---

## 6. 참고 자료
- [Ultralytics YOLOv8 공식 문서](https://docs.ultralytics.com/)
- [YOLO 데이터셋 포맷 설명](https://docs.ultralytics.com/datasets/detect/) 