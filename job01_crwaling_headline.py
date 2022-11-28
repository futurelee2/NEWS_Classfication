from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'} #딕셔너리 형태로 적어야함
#headers 내용: 서버 페이지> 오른쪽마우스 검사> network> name 에 아무거나 클릭하면 맨 밑에 Request Headers 에 User-Agent

df_titles = pd.DataFrame()
for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url,headers=headers) #서버한테 무엇을 요청하고 응답을 resp(응답 클래스 객체) 로 받음
    print(type(resp))
    # print(list(resp)) #rnrnrn (줄바꿈&커서 맨앞)이 화면상에서 생략됨
    soup = BeautifulSoup(resp.text, 'html.parser') #뷰티풀 숩: html 문서형태로 바꿔줌
    # print(soup)
    title_tags = soup.select('.cluster_text_headline') #앞에 .  붙이면 클래스 > 찾아서 리스트로
    titles = []
    #print(title_tags[0].text)
    for title_tag in title_tags:
        title = title_tag.text
        title = re.compile('[^가-힣0-9a-zA-Z ]').sub(' ',title) #^반전 / ^A-Z 빼고 전부다/A-Z 빼라 > sub '' 대신 이걸 넣어라/ # ^가-힣: 한글
        titles.append(title) #실제 사람들이 쓰는 말: 자연어
    df_section_titles = pd.DataFrame(titles, columns=['title'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows',ignore_index=True) #인덱스 무시
print(df_titles)
print(df_titles.category.value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
                 datetime.datetime.now().strftime('%Y%m%d')),index=False)

