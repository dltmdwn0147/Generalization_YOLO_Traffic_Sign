import os
import random
import shutil
from collections import defaultdict

# 데이터 폴더 경로 설정
image_folder = r"C:\Users\이승주\Desktop\한국_교통_표지판_인식_모델_프로젝트\Data_Set\YOLO_Data\All\images"   # 이미지 파일들이 있는 폴더 경로
label_folder = r"C:\Users\이승주\Desktop\한국_교통_표지판_인식_모델_프로젝트\Data_Set\YOLO_Data\All\labels"   # 라벨 텍스트 파일들이 있는 폴더 경로

# 하이퍼파라미터 설정
train_max = 800
test_max = 100
valid_max = 100
label_classes = 22  # 라벨 클래스 개수

# 이미지 및 라벨 파일 수집
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')])
label_files = sorted([f for f in os.listdir(label_folder) if f.endswith('.txt')])

# 라벨 개수 수집 및 데이터 딕셔너리 생성
label_count = defaultdict(int)
label_to_files = defaultdict(list)

# 각 파일에서 라벨 읽어오기
for label_file in label_files:
    with open(os.path.join(label_folder, label_file), 'r') as f:
        labels = [line.split()[0] for line in f.readlines()]
        for label in labels:
            label_count[label] += 1
            label_to_files[label].append(label_file)

# 스몰 데이터셋 생성 함수
def create_small_dataset(label_to_files, max_counts, min_counts=1):
    small_dataset = []
    for label, files in label_to_files.items():
        # 라벨별로 필요한 파일 수 제한
        if len(files) < min_counts:
            selected_files = files  # 최소 개수 이하라면 전체 파일 선택
        else:
            selected_files = random.sample(files, min(len(files), max_counts))
        small_dataset.extend(selected_files)
    
    # 전체 개수 제한 (max_counts 초과 시 랜덤으로 개수 조정)
    if len(small_dataset) > max_counts:
        small_dataset = random.sample(small_dataset, max_counts)
    
    return small_dataset

# 각 데이터셋에 대한 파일 수 결정
train_labels = create_small_dataset(label_to_files, train_max)
test_labels = create_small_dataset(label_to_files, test_max)
valid_labels = create_small_dataset(label_to_files, valid_max)

# 타겟 폴더 초기화 함수
def initialize_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # 폴더 및 내부 모든 파일 삭제
    os.makedirs(folder_path, exist_ok=True)  # 빈 폴더 생성

# 파일 복사 및 저장 경로 지정
def save_files(label_files, target_folder):
    # 폴더 초기화 (이미지와 라벨 폴더를 각각 초기화)
    image_target_folder = os.path.join(target_folder, 'images')
    label_target_folder = os.path.join(target_folder, 'labels')
    initialize_folder(image_target_folder)
    initialize_folder(label_target_folder)
    
    for label_file in label_files:
        # 라벨 파일 복사
        label_src = os.path.join(label_folder, label_file)
        label_dst = os.path.join(label_target_folder, label_file)
        shutil.copy2(label_src, label_dst)
        
        # 이미지 파일 복사
        image_file = label_file.replace('.txt', '.jpg')  # 필요에 따라 확장자 조정
        image_src = os.path.join(image_folder, image_file)
        image_dst = os.path.join(image_target_folder, image_file)
        if os.path.exists(image_src):
            shutil.copy2(image_src, image_dst)
        else:
            print(f"이미지 파일 {image_file}를 찾을 수 없습니다.")

# 결과 저장 경로 생성 및 초기화
save_files(train_labels, r'C:\Users\이승주\Desktop\test_data_set_v2\train')
save_files(test_labels, r'C:\Users\이승주\Desktop\test_data_set_v2\test')
save_files(valid_labels, r'C:\Users\이승주\Desktop\test_data_set_v2\valid')

print("Train, Test, Valid 데이터셋이 성공적으로 생성되었습니다.")
