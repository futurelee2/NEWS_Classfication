from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import re
import pandas as pd
import datetime

#chromdriver 다운받기 (chrom 버전 확인: 도움말>크롬정보에서 확인)
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
# pages = [167,377,505,71,94,73] #데이터의 불균형 맞춰주기: 적은것 늘려서 중복데이터만들기 or 많은 것을 줄이기
pages = [101,101,101,71,94,73] #적은카테고리의 마지막엔 자료가 다 없을 수 있어서 마지막 페이지 빼줘야함 + range 범위설정할때 1 더해야함
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=2'

options = webdriver.ChromeOptions()
#options.add_argument('headless') #이거하면 브라우저 안띄워짐
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver',options=options) #driver : 크롬브라우져 띄움
df_title = pd.DataFrame()


#주소가 명확해서 for문 가능
#x_path =
#'//*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a'
#'//*[@id="section_body"]/ul[1]/li[2]/dl/dt[2]/a'
#'//*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a' #ul[1]li[5] 넘어가면 ul[2]li[1]로바뀜

for i in range(4,6): #section
    titles = []
    for j in range(1,pages[i]): # 페이지
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i,j)
        driver.get(url)
        time.sleep(0.2)  # 0.2초안 띄워져있다가 꺼짐

        for k in range(1,5): # x_path
            for l in range(1,6): # x_path
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k,l) #이미지 있으면
                try:
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ',title)
                    titles.append(title)
                except NoSuchElementException as e:
                    try:
                        x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k,l) #이미지 없으면
                        title = driver.find_element('xpath', x_path).text
                        title = re.compile('[^가-힣 ]').sub(' ',title)
                        titles.append(title)
                    except:
                        print('error', i, j, k, l)
                except:
                    print('error', i, j, k, l)

        if j % 10 == 0: #10페이지마다 저장
            df_section_title = pd.DataFrame(titles, columns=['title'])
            df_section_title['category'] = category[i]
            df_title = pd.concat([df_title, df_section_title], ignore_index=True)
            df_title.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(category[i],j),
                            index = False)
            titles = [] #중복되지 않게


