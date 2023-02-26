import numpy as np
import cv2
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb, name_to_rgb
import color_rgb


def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'closest match: {names[index]}'


# RGB 색깔 판단 해주는 함수
# print(convert_rgb_to_names((55,18,17)))

def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


def image_color_cluster(image_path, k=3):
    # RGB
    list1 = [255, 0, 0]
    list2 = [255, 127, 0]
    list3 = [255, 212, 0]
    list4 = [0, 153, 0]
    list5 = [0, 0, 255]
    list6 = [75, 0, 130]
    list7 = [139, 0, 255]
    list8 = [0, 0, 0]
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    color_name_list = []
    clt = KMeans(n_clusters=k)
    clt.fit(image)
    # clt 히스토그램 수치 표에 따른 클러스터 rgb 정보
    hist = centroid_histogram(clt)
    hist = np.array(hist)
    print("속성 값: ", hist)
    print(np.where(hist == max(hist))[0])
    # 비중이 높은 색깔 뽑아내는 방법 index 추적은 np.where 사용
    bar = plot_colors(hist, clt.cluster_centers_)

    print(clt.cluster_centers_[np.where(hist == max(hist))[0]])
    print(convert_rgb_to_names((clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0],
                                clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1],
                                clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])))
    ###### color 이름 담기 위한 리스트
    color_name_list.append(convert_rgb_to_names((clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0],
                                                 clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1],
                                                 clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])))
    print(color_name_list[0][15:])
    if color_name_list[0][15:] in color_rgb.rgb_1:
        print("빨강")
    if color_name_list[0][15:] in color_rgb.rgb_2:
        print("노랑")
    if color_name_list[0][15:] in color_rgb.rgb_3:
        print("녹색")
    if color_name_list[0][15:] in color_rgb.rgb_4:
        print("청록")
    if color_name_list[0][15:] in color_rgb.rgb_5:
        print("청색")
    if color_name_list[0][15:] in color_rgb.rgb_6:
        print("보라")
    if color_name_list[0][15:] in color_rgb.rgb_7:
        print("핑크")
    if color_name_list[0][15:] in color_rgb.rgb_8:
        print("하얀색")
    if color_name_list[0][15:] in color_rgb.rgb_9:
        print("검정색")
    color_name = color_name_list[0][15:]
    print(name_to_rgb(color_name))
    # print(max(hist)+clt.cluster_centers_)
    # print(hist.index(max(hist)))

    ######image open#######

    # plt.figure()
    # plt.axis("off")
    # plt.imshow(bar)
    # plt.show()

import os

path = ""
for i in os.listdir('image/'):
    image_path = 'image\\'+i
    # preview image
    image = mpimg.imread(image_path)
    plt.imshow(image)

    image_color_cluster(image_path)


'''
 print("1: ",list1[0]-clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0]
          +list1[1]-clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1]
          +list1[2]-clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])
    print("2: ", list2[0] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0]
          + list2[1] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1]
          + list2[2] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])
    print("3: ", list3[0] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0]
          + list3[1] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1]
          + list3[2] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])
    print("4: ", list4[0] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0]
          + list4[1] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1]
          + list4[2] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])
    print("5: ", list5[0] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0]
          + list5[1] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1]
          + list6[2] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])
    print("6: ", list6[0] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0]
          + list6[1] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1]
          + list6[2] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])
    print("7: ", list7[0] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0]
          + list7[1] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1]
          + list7[2] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])
    print("8: ", list8[0] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][0]
          + list8[1] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][1]
          + list8[2] - clt.cluster_centers_[np.where(hist == max(hist))[0]][0][2])
'''
'''
list1 =[255, 0, 0]
list2  =[255, 127, 0]
list3  =[255, 212, 0]
list4  =[0,153, 0]
list5  =[0,0,255]
list6  =  [75,0,130]
list7  =[139, 0, 255]
list8  =[0, 0, 0]
'''
