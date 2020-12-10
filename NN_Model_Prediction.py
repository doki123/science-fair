from joblib import load
import os
import cv2
clf = load('apple_model.joblib')
pic_label = {}
apple_list = os.listdir('static/images')
for img_predict in apple_list:
    img_array = cv2.imread('static/images/' + img_predict)
    flat_img_array = cv2.resize(img_array, (50, 50))
    flat_img_array = flat_img_array.flatten()
    predict_apple = clf.predict([flat_img_array])
    predict_apple = predict_apple[0]  # brings prediction out of array
    pic_label.__setitem__(img_predict, predict_apple)
