import cv2
import matplotlib.pyplot as plt
import yaml

def plot_bounding_boxes(image_path, label_path, class_names):
    # 이미지 읽기
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    # 라벨 파일 읽기
    with open(label_path, 'r') as file:
        lines = file.readlines()

    # 각 라벨에 대해 바운딩 박스 그리기
    for line in lines:
        # YOLO 형식: class x_center y_center width height
        # 각 라벨 파일의 한 줄을 처리하여 여러 값을 추출
        values = line.strip().split()
        class_id = int(values[0])
        x_center = float(values[1])
        y_center = float(values[2])
        w = float(values[3])
        h = float(values[4])

        # 상대 좌표를 절대 픽셀 좌표로 변환
        x_center *= width
        y_center *= height
        w *= width
        h *= height

        # 바운딩 박스 좌표 계산
        x1 = int(x_center - w / 2)
        y1 = int(y_center - h / 2)
        x2 = int(x_center + w / 2)
        y2 = int(y_center + h / 2)

        # 바운딩 박스 그리기
        cv2.rectangle(image, (x1, y1), (x2, y2), color=(255, 0, 0), thickness=2)
        # 클래스 이름 표시
        if class_id < len(class_names):
            cv2.putText(image, class_names[class_id], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print(class_names[class_id])

    # 이미지 출력
    plt.imshow(image)
    plt.axis('off')
    plt.show()

# 클래스 이름 리스트
yaml_root = '/content/drive/MyDrive/Traffic_Sign_Recognition_Real_Time_Project/Data_Set/vtar(1918)/data.yaml'
with open(yaml_root) as f:
    file = yaml.full_load(f)
class_names = file['names']  # 실제 클래스 이름들로 대체  # names에 대한 값을 바꾸어도 문제 없음, 파악 후 바로 바꾸고 실행해도 됌.

# 예시 이미지와 라벨 파일 경로
img = 'signdataset-173-_jpg.rf.bd2ac0d2c399ad54f93c54334080bacc'
image_path = '/content/drive/MyDrive/Traffic_Sign_Recognition_Real_Time_Project/Data_Set/vtar(1918)_trans/valid/images/' + img + '.jpg'
label_path = '/content/drive/MyDrive/Traffic_Sign_Recognition_Real_Time_Project/Data_Set/vtar(1918)_trans/valid/labels/' + img + '.txt'

plot_bounding_boxes(image_path, label_path, class_names)