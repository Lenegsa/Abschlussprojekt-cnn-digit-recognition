from PIL import Image
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  #'Agg' no GUI
import io
import base64

# Load modell
model = load_model('./models/number_recognition_model_noisy_5.h5')

def predict_digit(image):
    
    # Image Preprocessing
    processed_result = preprocess_image(image)
    
    #Get the image
    processed_img = processed_result[0]
    grayscale_image = processed_result[1]
    
    # predict
    prediction = model.predict(processed_img)
    predicted_digit = np.argmax(prediction[0])
    confidence = np.max(prediction[0]) * 100
    
    print(f"Predict: {predicted_digit}, Confidence: {confidence:.2f}%")
    print(prediction[0])
    
    predictionImg = create_visualization(prediction[0])
   
    
    return predicted_digit, confidence, predictionImg, grayscale_image

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
    
    fig, ax = plt.subplots(figsize=(3,3))
    ax.set_title("Processed Image")
    ax.imshow(img_array,cmap='gray')
    ax.axis('off')
    
    
    # save to BytesIO png 
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    
    # convert to base 64
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
    
    # make dataURI 
    grayscale_img_data = f"data:image/png;base64,{img_base64}"
    
    # close plot
    plt.close(fig)
    
    # reshape to modell
    return img_array.reshape(1, 28, 28, 1), grayscale_img_data


def create_visualization(predictions):
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Make a graph
    labels = [f"{i}" for i in range(10)]
    ax.bar(labels, predictions*100, color='blue')
    ax.set_title("Predicted number: " + str(np.argmax(predictions)))
    ax.set_ylabel("Probability %")
    ax.set_xlabel("Numbers")
    bars = ax.bar(labels, predictions*100)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,  # x position (center of column)
            height + 0.01,                      # Y position (above the top of the column)
            f'{height:.2f}%',                    # Text (2 decimal places)
            ha='center',                        # Horizontal alignment
            va='bottom',                        # Vertical alignment
            fontsize=9                          # font size
        )
    
    # save to BytesIO png 
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    
    # convert to base 64
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
    
    # make dataURI 
    img_data = f"data:image/png;base64,{img_base64}"
    
    # close plot
    plt.close(fig)
    
    return img_data


