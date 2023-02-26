from flask import Flask, jsonify
# from app import *

# app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

import pymysql
from haversine import haversine

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='1234',
                       db='image_test',
                       charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

sql = "select La,Lo from dum"
curs.execute(sql)
result = curs.fetchall()
sql11 = "select user_la,user_lo from user_position"
curs.execute(sql11)
result1 = curs.fetchall()
la = result1[0]["user_la"]
lo = result1[0]["user_lo"]
print(la, lo)
users = (la, lo)
chk = "update image_test.dum set compare =%s where id =%s"

for i in range(len(result)):
    distance_com = (result[i]["La"], result[i]["Lo"])
    soo = haversine(users, distance_com, unit='m')
    curs.execute(chk, (soo, i + 1))
    conn.commit()
list_sql = "select id, store, compare from dum";
curs.execute(list_sql)
list_result = curs.fetchall()
print(list_result)
# 거리순 정렬
Store_sorted_dict = sorted(list_result, key=lambda x: (x['compare']))
compare_list = []
for i in range(len(Store_sorted_dict)):
    if Store_sorted_dict[i]['compare'] < 1480.49817:
        compare_list.append(Store_sorted_dict[i]['store'])

print("===================================", compare_list)

# Learning
import pandas as pd  # raw dataset
from surprise import SVD, accuracy  # SVD model, 평가
from surprise import Reader, Dataset  # SVD model의 dataset
from surprise.model_selection import cross_validate


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# 해천빌딩						35.1682089010283,129.17513636633
rating = pd.read_csv("Sample_GPS, menu_20220223.csv", encoding='cp949')
print("rating\n", rating)
print(rating['user'].value_counts(), rating['menu'].value_counts())
tab1 = pd.crosstab(rating['user'], rating['menu'])
print("tab1\n", tab1)
# movie rating
# 두 개의 집단변수를 가지고 나머지 rating을 그룹화
rating_g = rating.groupby(['user', 'menu'])
rating_g.sum()
tab = rating_g.sum().unstack()  # 행렬구조로 변환
print("tab\n", tab)
reader = Reader(rating_scale=(5, 10))  # 평점 범위
data = Dataset.load_from_df(df=rating, reader=reader)
# rating이라는 데이터프레임은 reader(1~5)의 평점 범위를 가진다.
print("data\n", data)
train = data.build_full_trainset()  # 훈련셋
test = train.build_testset()  # 검정셋

# %#%#%#%#%#%#%#% USER_PICK #%#%#%#%#%#%#%#%
# 음식
user_pick = "Food159"  # 입력이 들어갈 부분
print("USER:", user_pick)

# compare_list 는 가게 이름
s1 = set(rating['menu'])  ## 전체 메뉴
s1 = list(s1)
print(s1[0].split(' ')[1])
res = []
for i in range(len(s1)):
    if (user_pick == s1[i].split(' ')[1] and (s1[i].split(' ')[0] in compare_list)):
        res.append(s1[i])
print(res)
# 문자열 슬라이싱 만약에 데이터가 스페이바로 들어온다면

# print("s1\n", s1)
# filtered_df = rating[rating.user.eq('User2')]
# filtered_df = filtered_df.astype(dtype='string')
# s2 = set(filtered_df['menu'].tolist())
# compare_list = set(compare_list)
# ############   유저가 원하는 음식을 선택하는 input 값 적용   ############
# res = list(s1 - compare_list)
# print(s1, s2)
# res.sort()
# print(res)

# n_factors 가 높으면 정확도가 높아지지만 과접합 문제가 발생 할 수도 있음
model = SVD(n_factors=300, n_epochs=500)
print("=" * 100)
print()
print()
print(color.BOLD + 'Learning!!!!!                ######  WAITING  ######' + color.END)
print()
print()
print("=" * 100)

print(cross_validate(model, data))
model.fit(train)  # model 생성

user_id = 'User2'  # 추천대상자
actual_rating = 0  # 실제 평점

a = []
b = {}
for item_id in res:
    b[model.predict(user_id, item_id, actual_rating)[1]] = model.predict(user_id, item_id, actual_rating)[3]
sorted_dict = sorted(b.items(), key=lambda item: item[1], reverse=True)
print(sorted_dict)
compare_list_2 = []
for i in range(len(sorted_dict)):
    compare_list_2.append(sorted_dict[i][0][0:3])
print(compare_list_2)
if compare_list in compare_list_2:
    print(compare_list)
Final_output = []
for i in range(len(sorted_dict)):
    Final_output.append(list(sorted_dict[i]))
import json

Final_output = json.dumps(Final_output, ensure_ascii=False)
print(Final_output)
# print(sorted_dict[0][0][0:3])
# Store_sorted_dict[i]['store']
