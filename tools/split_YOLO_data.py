import os
import shutil
import glob
from sklearn.model_selection import train_test_split

# 원본 이미지와 라벨 폴더 경로
image_folder = r"C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\before_split_images"
label_folder = r"C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\before_split_labels"

# 분할된 데이터셋이 저장될 폴더 경로
train_image_dest = r'C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\split(4,3,3)\train\images'
train_label_dest = r'C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\split(4,3,3)\train\labels'
valid_image_dest = r'C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\split(4,3,3)\valid\images'
valid_label_dest = r'C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\split(4,3,3)\valid\labels'
test_image_dest = r'C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\split(4,3,3)\test\images'
test_label_dest = r'C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\split(4,3,3)\test\labels'

# 필요한 디렉토리 생성
os.makedirs(train_image_dest, exist_ok=True)
os.makedirs(train_label_dest, exist_ok=True)
os.makedirs(valid_image_dest, exist_ok=True)
os.makedirs(valid_label_dest, exist_ok=True)
os.makedirs(test_image_dest, exist_ok=True)
os.makedirs(test_label_dest, exist_ok=True)

# 모든 이미지 파일 목록을 가져와서 데이터셋 나누기
image_files = glob.glob(os.path.join(image_folder, '*.jpg'))

# 먼저 전체 데이터에서 80%는 train, 20%는 (test + valid)로 분할
train_files, valid_files = train_test_split(image_files, train_size=0.4, random_state=42)

# # 나머지 20%에서 50%를 valid, 나머지 50%를 test로 분할
valid_files, test_files = train_test_split(valid_files, test_size=0.5, random_state=42)

# 이미지 및 라벨 파일 복사 함수
def copy_images_and_labels(file_list, image_dest, label_dest):
    for image_path in file_list:
        # 이미지 파일 이름
        image_name = os.path.basename(image_path)
        # 라벨 파일 경로 (.jpg 대신 .txt로 변경)
        label_path = os.path.join(label_folder, image_name.replace('.jpg', '.txt'))
        
        # 이미지와 라벨 파일 복사
        if os.path.exists(image_path):
            shutil.copy(image_path, image_dest)
        if os.path.exists(label_path):
            shutil.copy(label_path, label_dest)

# train, valid, test 세트로 이미지와 라벨 파일 복사
copy_images_and_labels(train_files, train_image_dest, train_label_dest)
copy_images_and_labels(valid_files, valid_image_dest, valid_label_dest)
copy_images_and_labels(test_files, test_image_dest, test_label_dest)

print("데이터셋이 성공적으로 분할되었습니다.")