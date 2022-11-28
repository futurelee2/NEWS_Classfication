#다중분류기 : onhotencoding? 해줘야함
#자연어 전처리
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

#형태소 단위로 잘라줘야함> okt(Open Korean Text):  자바언어로 되어있어서 자바 설치 필요
# https://www.oracle.com/java/technologies/downloads/#jdk17-mac : 자바1.7 설치 (Konlpy)
# 참고: https://konlpy.org/ko/latest/install/
# 자바 설치 후 > pip install konlpy
# 시스템 > 고급시스템설정> (고급) 환경변수> (시스템변수) 새로만들기 클릭 후 자바 설치 경로 추가(변수이름: JAVA_HOME)
# (시스템변수) Path> (환경변수 편집) '%JAVA_HOME%\bin' 추가

from konlpy.tag import Okt
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./crawling_data/naver_news_titles_20221124.csv')
print(df.head(10))
print(df.category.value_counts())
df.info()

X = df['title']
Y = df['category']

encoder = LabelEncoder() #오름차순 정렬
labeled_Y = encoder.fit_transform(Y) #문자열을 숫자로 변환함
print(labeled_Y[:5])
print(encoder.classes_)
with open('./models/label_encoder.pickle','wb') as f: #encoder 저장
    pickle.dump(encoder, f) #onehot엔코딩하기 위해서?
onehot_Y = to_categorical(labeled_Y)
print(onehot_Y[:5])

okt = Okt() #형태소(의미를 가진 가장 작은 최소단위) 단위로 잘라주기

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)  # stem :  동사원형으로 바꿔줌 ex) 찾니 > 찾다
    if i % 100 == 0: #100의 배수가 될 때마다(=100문장) 점찍기
        print('.', end='')
    if i % 10000 == 0:
        print()

#한글자(조사,단어 등) 버리기 : 불용어(소용없는 형태소들)를 모아둔 것을 다운받기(stopwords.csv)
stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1: # 한글자보다 많은 것만
            if X[j][i] not in stopwords['stopword']: #불용어 리스트에 없으면 추가해라
                words.append(X[j][i])
    X[j] = ' '.join(words) #띄어쓰기 기준으로 하나의 문장 만들어줌
    #print(X[j])

token = Tokenizer() # X (형태소)의 유니크값 다 뽑아서 번호 줌 (1번부터 시작) back of words (BOW)
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1
with open('./models/news_token.pickle','wb') as f: #같은 단어 같은 숫자 주기 위해서 저장해줘야함
    pickle.dump(token,f)

#print(tokened_X)
#print(wordsize)

#문장의 길이가 다르기때문 shape을 정해줘야함 > 제일 긴문장에 맞추기
#짧은애들은 모자란 숫자만큼 0을 넣어서 긴문장에 맞춤> 그래서 1번부터 숫자시작도록 0 빼둠

max_len = 0
for i in range(len(tokened_X)):
    if max_len < len(tokened_X[i]):
        max_len = len(tokened_X[i])
print(max_len)

X_pad = pad_sequences(tokened_X, max_len)  #짧은 친구에게 padding을 입혀서 제일 긴문장에 맞춤
#print(X_pad)

X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./models/news_data_max_{}_wordsize_{}.npy'.format(max_len,wordsize),xy)




