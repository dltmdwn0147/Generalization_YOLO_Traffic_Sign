import os
import shutil
import random

# 원본 폴더 경로
images_folder = r"C:\Users\이승주\Desktop\nd_data\nd_all\before_split_images"
labels_folder = r"C:\Users\이승주\Desktop\nd_data\nd_all\before_split_labels"

# 비율 설정 (예: 데이터의 50%만 샘플링)
sampling_ratio = 0.3 # 남는 데이터의 비율

# 샘플링 후 데이터를 저장할 새로운 폴더 경로
output_images_folder = r"C:\Users\이승주\Desktop\reducing_ratio_v2_B\reducing_ratio_images_0.9"
output_labels_folder = r"C:\Users\이승주\Desktop\reducing_ratio_v2_B\reducing_ratio_labels_0.9"

# 폴더 생성 (이미 존재하면 건너뜀)
os.makedirs(output_images_folder, exist_ok=True)
os.makedirs(output_labels_folder, exist_ok=True)

# 이미지와 라벨 파일 목록 불러오기
image_files = sorted([f for f in os.listdir(images_folder) if f.endswith('.jpg') or f.endswith('.png')])
label_files = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])

# 이미지와 라벨 파일 수 확인
assert len(image_files) == len(label_files), "이미지 파일과 라벨 파일 수가 일치하지 않습니다."

# 파일 목록을 무작위로 섞음
file_pairs = list(zip(image_files, label_files))
random.shuffle(file_pairs)  # 목록을 무작위로 섞기

# 지정된 비율만큼 파일 선택
selected_files = file_pairs[:int(len(file_pairs) * sampling_ratio)]

# 선택된 파일을 새 폴더로 복사
for img_file, lbl_file in selected_files:
    shutil.copy(os.path.join(images_folder, img_file), os.path.join(output_images_folder, img_file))
    shutil.copy(os.path.join(labels_folder, lbl_file), os.path.join(output_labels_folder, lbl_file))

print(f"선택된 파일 {len(selected_files)}개가 {output_images_folder} 및 {output_labels_folder}에 저장되었습니다.")