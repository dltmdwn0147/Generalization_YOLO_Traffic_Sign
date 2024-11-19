from ultralytics import YOLO
import matplotlib.pyplot as plt
import os
import torch
import time

# CUDA가 사용 가능한지 확인
if torch.cuda.is_available():
    device = torch.device("cuda:0")  # 첫 번째 GPU 사용
    print('GPU 사용')
else:
    device = torch.device("cpu")  # CPU 사용
    print('CPU 사용')
# GPU를 사용할 때 변수가 필요할 경우 device를 사용

# if __name__ == '__main__':
# 데이터셋 경로
data_path = '/Users/이승주/Desktop/YOLO_DATA_SET/All(ACD)/split(4,3,3)/data.yaml'  # 사용하고자 하는 데이터셋 폴더
# 저장할 경로
save_dir = 'YOLOv5'

# 모델 초기화
model = YOLO("yolov5s.pt")  # 원하는 YOLO 모델 파일을 로드합니다

# 모델 학습
start = time.time()
name = 'All(ACD)(4,3,3)'
model.train(data = data_path, epochs = 50, imgsz = 640, project = save_dir, name = name, device = device, workers = 0)
print('학습 시간 : ', time.time() - start)