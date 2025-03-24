from PIL import Image
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Load modell
#model = load_model('number_recognition_model_noisy_5.h5')
model = load_model('./models/number_recognition_model_noisy_5.h5')

def preprocess_image(image_path):
    # Load image with PiL 
    img = Image.open(image_path).convert('L')  # greyscale
    
    # Resize 28*28
    img = img.resize((28, 28))
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Invert to black number - white background => white number, black background
    img_array = 255 - img_array
    
    # Normalisation
    img_array = img_array / 255.0
    
    # Show this picture
    plt.figure(figsize=(3, 3))
    plt.imshow(img_array, cmap='gray')
    plt.title("Picture to predict ")
    plt.axis('off')
    plt.show()
    
    # reshape to modell
    return img_array.reshape(1, 28, 28, 1)

def predict_digit(image_path):
    # Image Preprocessing
    img = preprocess_image(image_path)
    
    # predict
    prediction = model.predict(img)
    predicted_digit = np.argmax(prediction[0])
    confidence = np.max(prediction[0]) * 100
    
    print(f"Predict: {predicted_digit}, Confidence: {confidence:.2f}%")
    
    # Show Probability
    plt.figure(figsize=(10, 4))
    plt.bar(range(10), prediction[0])
    plt.xticks(range(10))
    plt.xlabel('Number')
    plt.ylabel('Probability')
    plt.title('Predicted number')
    plt.show()
    
    return predicted_digit, prediction[0]
