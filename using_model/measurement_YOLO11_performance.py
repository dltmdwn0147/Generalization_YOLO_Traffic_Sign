from ultralytics import YOLO
import matplotlib.pyplot as plt
import torch
import os

# CUDA가 사용 가능한지 확인
if torch.cuda.is_available():
    device = torch.device("cuda:0")  # 첫 번째 GPU 사용
    print('GPU 사용')
else:
    device = torch.device("cpu")  # CPU 사용
    print('CPU 사용')
# GPU를 사용할 때 변수가 필요할 경우 device를 사용

# 모델 로드
model = YOLO(r'C:\Users\이승주\Desktop\YOLOv11\All(test_0.3)\weights\best.pt')

# 저장할 경로 및 기본 설정
name = 'All(test_0.3_val)'
save_dir = r'C:\Users\이승주\Desktop\YOLOv11'

# 검증 수행
# data = r'C:\Users\이승주\Desktop\reducing_ratio_v2_B\reducing_ratio_0.9\data.yaml'
metrics = model.val(project = save_dir, name = name, device = device) # data = data, device = device, project = save_dir, name = name

# 메소드 호출
mean_results = metrics.mean_results()  # mean_results 메소드를 호출합니다.

# 주요 성능 지표 출력
print("평균 Precision:", mean_results[0])  # Precision
print("평균 Recall:", mean_results[1])     # Recall
print("mAP 50:", mean_results[2])          # mAP 50
print("mAP 50-95:", mean_results[3])       # mAP 50-95

# F1 Score와 FPS 추가로 출력
mean_f1_score = sum(metrics.box.f1) / len(metrics.box.f1)
print("FPS:", metrics.speed['inference'])    # FPS
print("F1 Score:", mean_f1_score)        # F1

# 그래프 시각화 (꺾이는 그래프, mAP 50-95)
iou_thresholds = list(range(50, 100, 5))
map_values = [metrics.box.maps[i] for i in range(len(iou_thresholds))]

plt.figure(figsize=(10, 5))
plt.plot(iou_thresholds, map_values, marker='o')
plt.title('mAP across IoU thresholds')
plt.xlabel('IoU Threshold (%)')
plt.ylabel('mAP')
plt.grid(True)
plt.show()