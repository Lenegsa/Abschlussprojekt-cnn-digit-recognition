from PIL import Image
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Load modell
#model = load_model('number_recognition_model_noisy_5.h5')
model = load_model('./models/number_recognition_model_noisy_5.h5')

def preprocess_image(getImage):
    # Load image with PiL 
    image = getImage
    img = Image.open(image).convert('L')  # greyscale  
    # Resize 28*28
    img = img.resize((28, 28))
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Invert to black number - white background => white number, black background
    img_array = 255 - img_array
    
    # Normalisation
    img_array = img_array / 255.0

    
    # reshape to modell
    return img_array.reshape(1, 28, 28, 1)

def predict_digit(image):
    # Image Preprocessing
    processedImg = preprocess_image(image)
    
    # predict
    prediction = model.predict(processedImg )
    predicted_digit = np.argmax(prediction[0])
    confidence = np.max(prediction[0]) * 100
    
    print(f"Predict: {predicted_digit}, Confidence: {confidence:.2f}%")
    print(prediction[0])
    
    return predicted_digit, confidence
