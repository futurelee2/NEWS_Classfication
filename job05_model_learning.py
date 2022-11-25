import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *

X_train, X_test, Y_train, Y_test = np.load(
    './models/news_data_max_20_wordsize_12063.npy', allow_pickle=True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

model = Sequential()
model.add(Embedding(12063,300,input_length=20)) #단어의 개수 =12063 차원/ 12063차원을 300차원으로 줄인다(=벡터라이징)
model.add(Conv1D(32,kernel_size=5,padding='same',activation='relu'))
model.add(MaxPool1D(pool_size=1)) #달라지는 것 어음
model.add(GRU(128,activation='tanh',return_sequences=True))
model.add(Dropout(0.3))
model.add(GRU(64,activation='tanh',return_sequences=True))
model.add(Dropout(0.3))
model.add(GRU(64,activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128,activation='relu'))
model.add(Dense(6,activation='softmax'))
model.summary()

# #차원이 늘어나면 데이터는 점점 희소해진다 (차원희소)/ 차원이 많아지면 값들이 더 멀어짐 > 차원을 줄여줘야함 : 좌표의 거리비가 유지되도록 (PCA/MDS)
#숫자를 준것을 학습시켜서 의미 파악? / 같은 단어는 같은 숫자 부여됨 / 의미공간의 좌표를 벡터로 씀
#word2vec

model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128,
                     epochs=10, validation_data=(X_test,Y_test))
model.save('./models/new_category_classfication_model_{}.h5'.format(
            np.round(fit_hist.history['val_accuracy'][-1],3)))
plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.show()
