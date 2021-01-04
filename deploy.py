import gradio as gr
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from transfer import load_model
from preprocessing import preprocess_image
# required library
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from local_utils import detect_lp
from os.path import splitext,basename
from keras.models import model_from_json
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet_v2 import preprocess_input
from sklearn.preprocessing import LabelEncoder
import glob
from segementing_Letter_Using_CV2 import DiffImage,sort_contours,get_Crop_Letter
from get_plate import get_plate


def predict_from_model(image,model,labels):
  image = cv2.resize(image,(80,80))
  image = np.stack((image,)*3, axis=-1)
  prediction = labels.inverse_transform([np.argmax(model.predict(image[np.newaxis,:]))])
  return prediction


def demo(img):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img = img/255
  wpod_net_path = "wpod-net.json"
  wpod_net = load_model(wpod_net_path)
  test_roi,crop_characters=get_Crop_Letter(wpod_net,img)
  #load pretrained
  #Load model architecture, weight and labels
  json_file = open('MobileNets_character_recognition.json', 'r')
  loaded_model_json = json_file.read()
  json_file.close()
  model = model_from_json(loaded_model_json)
  model.load_weights("License_character_recognition_weight.h5")
  print("[INFO] Model loaded successfully...")
  labels = LabelEncoder()
  labels.classes_ = np.load('license_character_classes.npy')
  print("[INFO] Labels loaded successfully...")

  # pre-processing input images and pedict with model

  final_string = ''
  for character in crop_characters:
    title = np.array2string(predict_from_model(character,model,labels))
    final_string+=title.strip("'[]")

  return 'Result: '+final_string


iface = gr.Interface(demo, gr.inputs.Image(), "text")
iface.launch()
# test_image_path = "Plate_examples/germany_car_plate.jpg"
# img=cv2.imread(test_image_path)
# print(demo(img))
#  return {'Binary type':binary},{'cropped Characters':crop_characters},{'final result':final_string}