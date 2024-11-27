from tflite_runtime.interpreter import Interpreter
from tqdm import tqdm
import cv2 as cv
import os
import numpy as np
from picamera2 import Picamera2

os.path.exists('plant.tflite')

def preview_start():
    try:
        picam2 = Picamera2()
        preview_config = picam2.create_preview_configuration()
        picam2.configure(preview_config)
        picam2.start_preview()
        picam2.stop_preview()
        return True
    except Exception as e:
        print("no monitor found!!!")
        return False
def image_prep(path):
  img = cv.imread(path)
  img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
  img = cv.resize(img, (224, 224))
  img = img.astype('float32') / 255.0
  img = img.reshape(1, 224, 224, 3)
  return img

interpret = Interpreter(model_path = 'plant.tflite')
interpret.allocate_tensors()
input_details = interpret.get_input_details()
output_details = interpret.get_output_details()

diseases = {
    "0": "Apple___Apple_scab",
    "1": "Apple___Black_rot",
    "2": "Apple___Cedar_apple_rust",
    "3": "Apple___healthy",
    "4": "Blueberry___healthy",
    "5": "Cherry_(including_sour)_Powdery_mildew",
    "6": "Cherry_(including_sour)_healthy",
    "7": "Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot",
    "8": "Corn_(maize)Common_rust",
    "9": "Corn_(maize)_Northern_Leaf_Blight",
    "10": "Corn_(maize)_healthy",
    "11": "Grape___Black_rot",
    "12": "Grape__Esca(Black_Measles)",
    "13": "Grape__Leaf_blight(Isariopsis_Leaf_Spot)",
    "14": "Grape___healthy",
    "15": "Orange__Haunglongbing(Citrus_greening)",
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
def run_with():
    capture = Picamera2()
    camera_config = capture.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
    capture.configure(camera_config)

    blank = np.zeros((224, 224, 3), dtype = 'uint8')
    frame_count = 0
    skip_frames = 10
    x = '38'
    capture.start()
    while True:
      Frame = capture.capture_array()
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

    capture.stop()
    cv.destroyAllWindows()
def run_without():
    picam2.start()
    time.sleep(2)
    img = picam2.capture_array()
    picam2.stop()
    img = cv.cvtColor(Frame, cv.COLOR_BGR2RGB)
    img = cv.resize(img, (224, 224))
    img = img.astype('float32') / 255.0
    img = img.reshape(1, 224, 224, 3)
    interpret.set_tensor(input_details[0]['index'], img)
    interpret.invoke()
    output_data = interpret.get_tensor(output_details[0]['index'])
    x = output_data[0].argmax()
    
    print(disease[str(x)])

if name == "main":
    if preview_start():
        run_with()
    else:
        run_without()
