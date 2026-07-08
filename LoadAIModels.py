from keras.models import load_model

#importing modules
import numpy as np
import keras
import tensorflow
import cv2
from keras.applications.resnet50 import preprocess_input
import os
import matplotlib.pyplot as plt

def LoadModels():
    wthr_param_model_path = "neural_networks\\Numeric Model\\Weather_parameters_model_firebias_v1.keras"
    image_model_path = "neural_networks\\Image Model\\Models\\wildfire_image_classification_v1_local.keras"

    #flag to check if the load is successfull
    error_occured = False
    #Loading models
    try:
        fire_weather_model = load_model(wthr_param_model_path)
    except Exception as e:
        error_occured = True
        print(f"Failed to load weather parameters model with error: {e}")
    try:
        resnet_preprocess = {'preprocess_input':preprocess_input}#{'module': 'builtins', 'class_name': 'function', 'config': 'preprocess_input', 'registered_name': 'function'}
        fire_image_model = load_model(image_model_path, custom_objects=resnet_preprocess) 
    except Exception as e:
        error_occured = True
        print(f"Failed to load image classification model with error: {e}")
    if error_occured == False:
        return error_occured, fire_weather_model, fire_image_model
    else:
        return error_occured, "", ""

def FireWeatherPredict(fire_w_model, input_data): # 1 - Fire, 0 - No Fire
    threshold = 0.3768
    prediction_prob = fire_w_model.predict(x=input_data)
    print("Model output: ", prediction_prob)
    predicted_class = (prediction_prob > threshold).astype(int)
    
    return prediction_prob, predicted_class

def FireImagePredict(fire_im_model, input_image_path): 
    threshold = 0.3889
    captured_image_bgr = cv2.imread(input_image_path)
    captured_image_rgb = cv2.cvtColor(captured_image_bgr, cv2.COLOR_BGR2RGB)
    resized_image = tensorflow.image.resize(captured_image_rgb, (224, 224))
    
    model_prediction = fire_im_model.predict(np.expand_dims(resized_image, 0))
    print("Model output: ", model_prediction)
    predicted_class = (model_prediction > threshold).astype(int)

    return model_prediction, predicted_class, resized_image

#status, fire_w_model, img_fire_model = LoadModels()
#print(status)

