import os
import pandas as pd

def polygon_to_bounding_box(polygon_coords):
    xs = [coord[0] for coord in polygon_coords]
    ys = [coord[1] for coord in polygon_coords]

    xmin = min(xs)
    ymin = min(ys)
    xmax = max(xs)
    ymax = max(ys)

    return xmin, ymin, xmax, ymax

def read_labels_from_txt(label_file):
    with open(label_file, 'r') as f:
        lines = f.readlines()

    coordinates = []
    for line in lines:
        parts = list(map(float, line.strip().split()))
        # 첫 번째 값은 클래스 ID, 나머지는 좌표
        class_id = int(parts[0])
        coords = [(parts[i], parts[i+1]) for i in range(1, len(parts), 2)]
        coordinates.append((class_id, coords))

    return coordinates

def create_csv_from_labels(images_dir, labels_dir, output_csv):
    rows = []
    for filename in os.listdir(images_dir):
        if filename.endswith(('.jpg', '.png')):  # 지원하는 이미지 형식
            label_file = os.path.join(labels_dir, f"{os.path.splitext(filename)[0]}.txt")
            if os.path.exists(label_file):
                labels = read_labels_from_txt(label_file)
                for class_id, polygon_coords in labels:
                    xmin, ymin, xmax, ymax = polygon_to_bounding_box(polygon_coords)
                    rows.append([filename, xmin, ymin, xmax, ymax, class_id])

    # DataFrame 생성 후 CSV로 저장
    df = pd.DataFrame(rows, columns=['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class'])
    df.to_csv(output_csv, index=False)

# 사용 예
create_csv_from_labels(images_dir='/content/drive/MyDrive/Traffic_Sign_Recognition_Real_Time_Project/Data_Set/Data_Set/vtar_merged/test/images',
                       labels_dir='/content/drive/MyDrive/Traffic_Sign_Recognition_Real_Time_Project/Data_Set/Data_Set/vtar_merged/test/labels',
                       output_csv='/content/drive/MyDrive/Traffic_Sign_Recognition_Real_Time_Project/Data_Set/Data_Set/vtar_merged/test/vtar_csv.csv')