from __future__ import absolute_import, division, print_function, unicode_literals
import cv2
import numpy as np 
import tensorflow as tf



model = tf.keras.models.load_model('image_ai/face-latest.hdf5', compile=False)
model.compile()
model.load_weights('image_ai/spoofing_weights.h5')



def check_spoofing(img):
    threshold = 0.5

    frame = cv2.resize(img, (224, 224))
    frame = frame / 255.0

    prediction = model.predict(np.expand_dims(frame, axis=0)) 
    y_pred = np.zeros(prediction.shape).astype(np.int32) 
    y_pred[prediction > threshold] = 1  
    print(y_pred[0])
    text = "Spoof" if y_pred[0] else "Real"
    return text