import tensorflow as tf
from tqdm import tqdm
import cv2 as cv
import os
import numpy as np

os.path.exists('1.tflite')

def image_prep(path):
  img = cv.imread(path)
  img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
  img = cv.resize(img, (224, 224))
  img = img.astype('float32') / 255.0
  img = img.reshape(1, 224, 224, 3)
  return img

interpret = tf.lite.Interpreter(model_path = '1.tflite')
interpret.allocate_tensors()
input_details = interpret.get_input_details()
output_details = interpret.get_output_details()

diseases = {
    "0": "Apple___Apple_scab",
    "1": "Apple___Black_rot",
    "2": "Apple___Cedar_apple_rust",
    "3": "Apple___healthy",
    "4": "Blueberry___healthy",
    "5": "Cherry_(including_sour)___Powdery_mildew",
    "6": "Cherry_(including_sour)___healthy",
    "7": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "8": "Corn_(maize)___Common_rust_",
    "9": "Corn_(maize)___Northern_Leaf_Blight",
    "10": "Corn_(maize)___healthy",
    "11": "Grape___Black_rot",
    "12": "Grape___Esca_(Black_Measles)",
    "13": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "14": "Grape___healthy",
    "15": "Orange___Haunglongbing_(Citrus_greening)",
    "16": "Peach___Bacterial_spot",
    "17": "Peach___healthy",
    "18": "Pepper_bell___Bacterial_spot",
    "19": "Pepper_bell___healthy",
    "20": "Potato___Early_blight",
    "21": "Potato___Late_blight",
    "22": "Potato___healthy",
    "23": "Raspberry___healthy",
    "24": "Soybean___healthy",
    "25": "Squash___Powdery_mildew",
    "26": "Strawberry___Leaf_scorch",
    "27": "Strawberry___healthy",
    "28": "Tomato___Bacterial_spot",
    "29": "Tomato___Early_blight",
    "30": "Tomato___Late_blight",
    "31": "Tomato___Leaf_Mold",
    "32": "Tomato___Septoria_leaf_spot",
    "33": "Tomato___Spider_mites Two-spotted_spider_mite",
    "34": "Tomato___Target_Spot",
    "35": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "36": "Tomato___Tomato_mosaic_virus",
    "37": "Tomato___healthy",
    "38" : "scan now!!"
}

"""## FOR DETECTION VIA CAM"""

capture = cv.VideoCapture(0)
blank = np.zeros((224, 224, 3), dtype = 'uint8')
frame_count = 0
skip_frames = 10
x = '38'
while True:
  isTrue, Frame = capture.read()
  frame_count += 1
  if frame_count % skip_frames == 0:
    img = cv.cvtColor(Frame, cv.COLOR_BGR2RGB)
    img = cv.resize(img, (224, 224))
    img = img.astype('float32') / 255.0
    img = img.reshape(1, 224, 224, 3)
    interpret.set_tensor(input_details[0]['index'], img)
    interpret.invoke()
    output_data = interpret.get_tensor(output_details[0]['index'])
    x = output_data[0].argmax()
  Frame = cv.putText(Frame, diseases[str(x)], (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

  cv.imshow('frame', Frame)

  if cv.waitKey(20) & 0xFF == ord('d'):
    break

capture.release()
cv.destroyAllWindows()
"""## FOR IMAGE DATA TO UPLOAD VIA FILES"""
"""
path = input('enter path of the file for detection: ')
input_data = image_prep(path)

interpret.set_tensor(input_details[0]['index'], input_data)
interpret.invoke()
output_data = interpret.get_tensor(output_details[0]['index'])
print(diseases[str(output_data[0].argmax())])
"""


