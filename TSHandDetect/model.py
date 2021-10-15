import os
import pickle
import tensorflow as tf
from sklearn.model_selection import train_test_split

DATA = []
LABELS = []

for i in os.listdir('.'):
    if i.split('.')[1] == 'ct':
        ii = i.split('.')[0]
        f = open(i, "rb")
        for d in pickle.load(f):
            temp = []
            for j in d:
                temp += d[j]
            DATA.append(temp)
            LABELS.append(int(ii))
print(len(DATA))
#raise SystemExit
NUM_CLASSES = 5

X_train, X_test, y_train, y_test = train_test_split(DATA,
    LABELS,
    test_size=0.33,
    random_state=42)

model = tf.keras.models.Sequential([
    tf.keras.layers.Input((21 * 3, )),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(60, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(45, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='relu'),
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    X_train,
    y_train,
    epochs=1000,
    batch_size=1024,
    validation_data=(X_test, y_test),
)

model.save('model.h5')
