import cv2 as cv
import matplotlib.pyplot as plt
import os
import yaml

label_folder = r'C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\before_split_labels' 
yaml_folder = r'C:\Users\이승주\Desktop\YOLO_DATA_SET\All(ACD)\data.yaml'

# 학습 시킬 라벨들의 개수 확인, 데이터셋의 data.yaml 파일에서 'nc'라는 key 값으로 value 값 추출
with open(yaml_folder) as f:
    film = yaml.load(f, Loader=yaml.FullLoader)
    print('학습시킬 라벨 총 개수 : ', film['nc'])
    print('학습 라벨 명 : ', film['names'])

# 라벨들을 하나의 리스트 변수에 저장
label_list = []

for txt_file in os.listdir(label_folder):
    with open(os.path.join(label_folder, txt_file), 'r') as file:
        content = file.read()

        if content.strip() == '':  # 라벨 텍스트 파일이 비어있을 경우 예외처리 (-1로 추가)
            label_list.append(-1)
            continue

        # 여러 라벨이 있을 수 있으므로 각 라인을 별도로 처리
        lines = content.splitlines()
        for line in lines:
            label = line.split()[0]  # 라벨 번호만 추출 (첫 번째 값)
            if label.isdigit():
                label_list.append(int(label))

print(label_list)
print('총 라벨 개수:', len(label_list))

# 라벨 별 개수 파악
label_count = []

for count in range(min(label_list), max(label_list) + 1):
    label_count.append(label_list.count(count))

# 라벨 그래프 그리기
x_line = [x for x in range(min(label_list), max(label_list) + 1)]  # x 축에 표현될 라벨들

print('fa883 / test / labels')  # 라벨 개수 파악할 때 어떤 데이터의 라벨인지 적어놓는 곳
print(label_count)

# 그래프 그리기 / .yaml 데이터셋 기준
plt.figure(figsize=(10, 8))
bar = plt.barh(film['names'], label_count, color='skyblue')

# Barh 그래프에서 막대 우측 부분에 수치 기입
for index, value in enumerate(label_count):
    plt.text(value, index, str(value), va='center')

# 그래프 설정
plt.xlabel('Count')  # 그래프에서 x 축 이름 설정
plt.ylabel('Label')  # 그래프에서 y 축 이름 설정
plt.title('Label Count Distribution')  # 그래프 제목 설정
plt.show()

# 라벨들의 총 개수 출력
print('라벨들의 총 개수 : ', len(label_list))