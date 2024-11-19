import os
import shutil

# 제외할 라벨 ID를 지정 (리스트로 여러 개의 라벨을 지정)
exclude_labels = [2]  # 예시: 라벨 2를 제외

# 원본 라벨 파일들이 있는 폴더 경로
label_folder_path = '/Users/이승주/Desktop/nd_data/C_class_reducing/labels'

# 필터링된 라벨 파일을 저장할 폴더
filtered_label_folder_path = '/Users/이승주/Desktop/nd_data/C_class_reducing/filtering_labels(2)/labels'
filtered_image_folder_path = '/Users/이승주/Desktop/nd_data/C_class_reducing/filtering_labels(2)/images'

# 원본 이미지 폴더 경로
image_folder_path = '/Users/이승주/Desktop/nd_data/C_class_reducing/images'

# 새로운 폴더 생성
os.makedirs(filtered_image_folder_path, exist_ok=True)
os.makedirs(filtered_label_folder_path, exist_ok=True)

# 추적용 카운터 초기화
moved_image_count = 0
moved_label_count = 0
deleted_image_count = 0
deleted_label_count = 0
deleted_labels_count = {}  # 삭제된 라벨을 추적할 딕셔너리

# 라벨 파일에서 특정 라벨 제외
for label_file in os.listdir(label_folder_path):
    # 확장자가 .txt인 파일만 처리
    if label_file.endswith('.txt'):
        input_path = os.path.join(label_folder_path, label_file).replace('\\', '/')
        output_path = os.path.join(filtered_label_folder_path, label_file).replace('\\', '/')
        
        # 새로운 라벨 데이터를 저장할 리스트
        filtered_data = []

        # 원본 라벨 파일을 읽고 특정 라벨 제외
        with open(input_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()  # 앞뒤 공백 제거
                if line == "":  # 빈 줄이면 건너뛰기
                    continue
                parts = line.split()  # 공백을 기준으로 라벨 정보 분리
                
                try:
                    label_id = int(parts[0])  # 라벨 ID는 첫 번째 요소 (정수로 변환)
                except ValueError:
                    print(f"잘못된 라벨 형식 발견: {line}")
                    continue  # 숫자가 아닌 라벨은 무시

                # 디버깅용 출력: 라벨 ID와 비교 대상 출력
                print(f"라인: {line} - 라벨 ID: {label_id}")

                if label_id not in exclude_labels:  # 제외할 라벨 ID가 아닌 경우만 추가
                    filtered_data.append(line)
                else:
                    # 삭제된 라벨 카운트 증가
                    if label_id in deleted_labels_count:
                        deleted_labels_count[label_id] += 1
                    else:
                        deleted_labels_count[label_id] = 1

        # 필터링된 데이터가 하나라도 있으면 새 파일에 저장
        if filtered_data:
            with open(output_path, 'w') as file:
                file.writelines(filtered_data)

            # 필터링된 텍스트 파일에 해당하는 이미지 파일을 images 폴더에 저장
            image_file = label_file.replace('.txt', '.jpg')
            image_path = os.path.join(image_folder_path, image_file).replace('\\', '/')

            if os.path.exists(image_path):
                # 이미지 파일을 필터링된 images 폴더로 복사
                shutil.copy(image_path, os.path.join(filtered_image_folder_path, image_file).replace('\\', '/'))
                moved_image_count += 1  # 이미지 이동 카운트 증가
            moved_label_count += 1  # 라벨 파일 이동 카운트 증가
        else:
            # 라벨 파일에 남은 데이터가 없으면 해당 텍스트 파일 삭제
            os.remove(input_path)  # 원본 텍스트 파일 삭제
            deleted_label_count += 1  # 삭제된 라벨 파일 카운트 증가

            # 이미지 파일 삭제 (이름은 동일하지만 확장자는 .jpg)
            image_file = label_file.replace('.txt', '.jpg')
            image_path = os.path.join(image_folder_path, image_file).replace('\\', '/')
            if os.path.exists(image_path):
                os.remove(image_path)  # 이미지를 삭제
                deleted_image_count += 1  # 삭제된 이미지 파일 카운트 증가

# 결과 출력
print(f"필터링된 이미지 파일 개수: {moved_image_count}")
print(f"필터링된 텍스트 파일 개수: {moved_label_count}")
print(f"삭제된 이미지 파일 개수: {deleted_image_count}")
print(f"삭제된 텍스트 파일 개수: {deleted_label_count}")
print(f"삭제된 라벨 개수: {deleted_labels_count}")
print("필터링 및 이동이 완료되었습니다.")