from app import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/RestAPI')
def population():
    import pymysql
    from haversine import haversine

    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234',
                           db='image_test',
                           charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql = "select La,Lo from store"
    curs.execute(sql)
    result = curs.fetchall()
    sql11 = "select user_la,user_lo from user_position"
    curs.execute(sql11)
    result1 = curs.fetchall()
    la = result1[0]["user_la"]
    lo = result1[0]["user_lo"]
    print(la, lo)
    users = (la, lo)
    chk = "update image_test.store set compare =%s where id =%s"

    for i in range(len(result)):
        distance_com = (result[i]["La"], result[i]["Lo"])
        soo = haversine(users, distance_com, unit='m')
        curs.execute(chk, (soo, i + 1))
        conn.commit()
    list_sql = "select id, store, compare from store";
    curs.execute(list_sql)
    list_result = curs.fetchall()
    print(list_result)
    # 거리순 정렬
    Store_sorted_dict = sorted(list_result, key=lambda x: (x['compare']))
    compare_list = []
    for i in range(len(Store_sorted_dict)):
        if Store_sorted_dict[i]['compare'] < 1500:
            compare_list.append(Store_sorted_dict[i]['store'])

    print(compare_list)

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
    reader = Reader(rating_scale=(3, 5))  # 평점 범위
    data = Dataset.load_from_df(df=rating, reader=reader)
    # rating이라는 데이터프레임은 reader(1~5)의 평점 범위를 가진다.
    print("data\n", data)
    train = data.build_full_trainset()  # 훈련셋
    test = train.build_testset()  # 검정셋

    # 4. model 생성
    # help(SVD)
    s1 = set(rating['menu'][:3])
    print(s1)
    filtered_df = rating[rating.user.eq('User2')]
    filtered_df = filtered_df.astype(dtype='string')
    s2 = set(filtered_df['menu'].tolist())
    compare_list = set(compare_list)
    res = list(s1 - compare_list)
    print(s1, s2)
    res.sort()
    print(res)
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
    # # 5. Toby 사용자 영화추천
    user_id = 'User2'  # 추천대상자

    actual_rating = 0  # 실제 평점

    a = []
    b = {}
    for item_id in res:
        b[model.predict(user_id, item_id, actual_rating)[1]] = model.predict(user_id, item_id, actual_rating)[3]
    sorted_dict = sorted(b.items(), key=lambda item: item[1], reverse=True)
    compare_list_2 = []
    for i in range(len(sorted_dict)):
        compare_list_2.append(sorted_dict[i][0][0:3])
    print(compare_list_2)
    if compare_list in compare_list_2:
        print(compare_list)
    print(sorted_dict)
    # print(sorted_dict[0][0][0:3])
    # Store_sorted_dict[i]['store']
    return jsonify(sorted_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="9999")
