# Crimson Snow, Golden, Golden-Red, Granny Smith, Pink Lady, Red, Red Delicious
# Citation: Horea Muresan, [Mihai Oltean](https://mihaioltean.github.io), [Fruit recognition from images using deep
# learning](https://www.researchgate.net/publication/321475443_Fruit_recognition_from_images_using_deep_learning),
# Acta Univ. Sapientiae, Informatica Vol. 10, Issue 1, pp. 26-42, 2018.

from sklearn import neighbors
from joblib import dump, load
import sklearn.model_selection
import numpy as np
import os
import cv2


test_folder = 'data/fruits-360/Test/'
train_folder = 'data/fruits-360/Training/'

test_dirs = os.listdir(test_folder)
train_dirs = os.listdir(train_folder)

data = []
labels = []
for sub_test_folder in test_dirs:
    for file_test in os.listdir(test_folder + sub_test_folder + '/'):
        test_img_array = cv2.imread(test_folder + sub_test_folder + '/' + file_test)
        flat_test_array = cv2.resize(test_img_array, (50, 50))
        flat_test_array = flat_test_array.flatten()
        data.append(flat_test_array)
        labels.append(sub_test_folder)

for sub_train_folder in train_dirs:
    for file_train in os.listdir(train_folder + sub_train_folder + '/'):
        train_img_array = cv2.imread(train_folder + sub_train_folder + '/' + file_train)
        flat_train_array = cv2.resize(train_img_array, (50, 50))
        flat_train_array = flat_train_array.flatten()
        data.append(flat_train_array)
        labels.append(sub_train_folder)

data = np.array(data)
labels = np.array(labels)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(data, labels, test_size=0.2)
clf = neighbors.KNeighborsClassifier()
clf.fit(x_train, y_train)
dump(clf, 'apple_model.joblib')
