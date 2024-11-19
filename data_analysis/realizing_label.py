import matplotlib.pyplot as plt
import os

image_folder = '/content/drive/MyDrive/Alldata(ACD)/before_split_images' ### 주소 변경 해야함 ###
label_folder = '/content/drive/MyDrive/Alldata(ACD)/before_split_labels' ### 주소 변경 해야함 ###
txt_folder = '/content/drive/MyDrive/Traffic_Sign_Recognition_Real_Time_Project/Data_Set/9vtar_trans/classes.txt' ### 그래프 그리기 파악 때만 vtar(1918)_trans .txt 파일 사용

# 학습 시킬 라벨들의 개수 확인, txt 파일에서 불러옴
label_txt_list = []
f = open(txt_folder, 'r')
for txt_line in f:
  label_txt_list.append(txt_line[:-1]) # txt 파일로 불러왔기 때문에 라벨마다의 뒤에 줄바꿈이 포함되어 있어서 줄바꿈(\n)을 제외하기 위해 [:-1]를 표시
print('학습시킬 라벨 총 개수 : ', len(label_txt_list))
print('학습 라벨 명 : ', label_txt_list)

# 라벨들을 하나의 리스트 변수에 저장
label_list = []

for txt_file in os.listdir(label_folder):
  if txt_file == '.DS_Store' or txt_file == '.ipynb_checkpoints' or txt_file == 'desktop.ini':
      continue

  with open(os.path.join(label_folder, txt_file), 'r') as file:
    content = file.read()

    # if content == '': # 라벨 텍스트 파일에 라벨링이 되어 있지 않은 데이터들을 예외처리함, -1이라는 숫자로 예외처리 하였음.
    #   label_list.append(-1)
    #   continue

    lines = content.splitlines()
    for txt in lines:
      label_list.append(int(txt[:2])) # yolo v5 모델에 학습시키기 위한 라벨 파일은 텍스트 파일로써 가장 앞에 라벨이 표현, 한자리 또는 두자리로 표현되고 그 다음 칸에는 빈칸이기에 [:2] 표현하여 데이터 받아오기

      # 라벨 별 개수 파악
label_count = []

for count in range(len(label_txt_list)):
  label_count.append(label_list.count(count))

# 라벨 그래프 그리기
x_line = [x for x in range(min(label_list), max(label_list) + 1)] # x 축에 표현될 라벨들

print('All Data / valid / labels') ### 라벨 개수  파악할 때 어떤 데이터의 라벨인지 적어놓는 곳, 변동해서 사용해야 함 ###
bar = plt.barh(label_txt_list, label_count) # 그래프 그리기

# Barh 그래프에서 막대 우측 부분에 수치 기입하기, 세로 그래프일 경우에는 Label 명에 대해서 잘 안보이기 때문에 가로 막대 그래프로 진행
for index, value in enumerate(label_count):
    plt.text(value, index, str(value), va = 'center')

plt.yticks(label_txt_list) # .txt 데이터셋 기준
plt.xlabel('Count') # 그래프에서 x 축 이름 설정
plt.ylabel('Label') # 그래프에서 y 축 이름 설정

# 라벨들의 개수, 가독성을 위함
print('라벨들의 총 개수 : ', len(label_list))