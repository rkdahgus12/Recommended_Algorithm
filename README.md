
# Recommended_Algorithm
Collaborative Filtering, Opencv Test
<div>
  <p align="center">
    <img width="800" src="result_video.gif"> 
  </p>
</div>



## 추천 알고리즘 종류
* #### 협업 필터링 (Collaborative Filtering : CF)
   * 구매/소비 패턴이 비슷한 사용자를 한 집단으로 보고 그 집단에 속한 소비자들의 취향을 추천하는 방식
   * UBCF (User Based CF) : 패턴이 비슷한 사용자를 기반으로 상품(Item) 추천
   * IBCF (Item Based CF) : 상품(Item)을 기반으로 연관성이 있는 상품(Item) 추천

* #### 내용기반 필터링 (Content-Based Filtering : CB)
  * 뉴스, 책 등 텍스트의 내용을 분석해서 추천하는 방식
  * 소비자가 소비하는 제품 중 텍스트 정보가 많은 제품을 대상으로 함
  * 텍스트 중에서 형태소(명사, 동사 등)를 분석하여 핵심 키워드를 분석하는 기술이 핵심
  
* #### 지식기반 필터링 (Knowledge-Based Filtering : KB)
  * 특정 분야에 대한 전문가의 도움을 받아서 그 분야에 대한 전체적인 지식구조를 만들고 이를 활용하는 방식

* #### SVD 기반 추천시스템
  * 사용자의 특징과 아이템의 특징 그리고 이 두 가지를 대표하는 대각행렬 추출
  * 대각 행렬의 특이값으로 차원을 축소 (데이터의 양 줄이기)
  * 아직 평가하지 않은 데이터에 대해서 평균값을 이용해 결측치를 채운 뒤 SVD를 이용해 점수 예측
  * 추천 시스템에서는 이 예측된 점수가 높은 아이템을 추천
  ![캡처](https://user-images.githubusercontent.com/71003685/221398979-156c68e5-9dc2-4ef6-b5f3-29d628818e37.PNG)
* #### 현 프로젝트는 Surprise 알고리즘을 활용하고, 더미셋을 만든 후, SVD 모델 형성 후 REST API로 테스트
---
### 결과


![캡처](https://user-images.githubusercontent.com/71003685/221399052-57f914bb-685c-4bac-9c74-9c0dbec914de.PNG)

- 추천 알고리즘 협업 필터링, 컨텐츠 필터링, 하이브리드 기반 구현 하였음.
- 구현한 내용을 어떤 데이터를 활용하여 나타낼 것이고, 필요한 부분이 무엇이 있는지 확인 필요
- 프로젝트에 Ai 시스템 어떤 것을 추가를 하면 효율성이 있을지 고안
- 추천 알고리즘 현재로써는 구현 완효 json 파일 Flask를 이용하여 추출 하는 소스, User, Food 입력에 따른 알고리즘 실행 소스 구현 완료
---
## 소스 설명
- image_processing.py 안에 찍어놓은 메인 부분 사진의 rgb의 포함 형태를 histogram으로 표현 해주면서 얼만큼의 비중을 차지 하고 있으며, 
3번째 중 가장 많이 비중을 차지한 rgb 색깔을 판단하여 약 9색의 메인 색 안에 Find 하게끔 하였음.
- haversine에 따라 현 거리 기준으로 더미셋에 해당하는 정보에 따라 추천 해주는 방식

---
## 이미지 프로세싱 및 유사도 비교(ORB, KAZE, AKAZE)

- Opencv.py
- 실행 목적: 음식에 대한 컨텐츠 기획으로 색깔별로 구별할 수 있는 분류화를 시키고 호불호를 확인하기 위한 알고리즘 구현
- histogram으로 표현하여 음식에 대한 색깔 함류를 분석했을 때, 문제점: 만약 겉과 그릇의 부분을 제외를 제대로 하지 못하면 비율에 대한 문제점이 생김.


![캡처](https://user-images.githubusercontent.com/71003685/221399377-2de56b65-e302-448d-8c91-e991fab54e76.PNG)




