from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  #'Agg' no GUI
import io
import base64

# Load modell
model = load_model('./models/keras_models/number_recognition_model_noisy_5.h5')   
layers_images = []     
    
"""
Get the image (BytesIO) from Flask server /predict
Predict the digit and give response to Flask server this is the (main) method
Return  predicted digit, confidence %, confidence graph img, pre processed img
"""
def predict_digit(image):
  
    try:
        # Image Preprocessing
        processed_result = preprocess_image(image)
        
        #Get the image
        processed_img = processed_result[0]
        grayscale_image = processed_result[1]
        
        # predict
        prediction = model.predict(processed_img)
        predicted_digit = np.argmax(prediction[0]) #get the max value
        confidence = np.max(prediction[0]) * 100
        
        print(f"Predict: {predicted_digit}, Confidence: {confidence:.2f}%")
        print(prediction[0])
        
        #make a graph with prediction numbers
        predictionImg = create_visualization(prediction[0])
        
        #clear the layers images
        layers_images.clear()
        
        #fill this array with new images (layers_featuremaps)
        layer_visualization(processed_img)
       
    except Exception as e:
      print("An error occurred while recognizing the number" , e)
    
    # predicted digit, confidence %, confidence graph img, pre processed img
    return predicted_digit, confidence, predictionImg, grayscale_image, layers_images


"""
Get image from perdict_digit
Preprocess the (BytesIO) image to tensor(predict) 
Return reshape to modell(tensor) and greyscale image (base64)
"""
def preprocess_image(getImage):
    
    try:
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
       
       if img_array is not None:
           fig, ax = plt.subplots(figsize=(3,3))
           ax.set_title("Processed Image")
           ax.imshow(img_array,cmap='gray')
           ax.axis('off')
    
           # Save to base64 using the new function
           grayscale_img_data = save_to_base64(fig)
       else:
           raise ValueError("Can't create the image")
    
    except OSError as e :
        print("Error loading image.", e)
        
    except ValueError as e :
        print(e)
        
    except Exception as e:
        print("An error occurred while preprocessing the image." , e)
        
    # reshape to modell and greyscale image
    return img_array.reshape(1, 28, 28, 1), grayscale_img_data


"""
Get predictions array
Create a graph with predictions numbers
Return graph image (base64)
"""
def create_visualization(predictions):
    
    try:
       if predictions is None or len(predictions) == 0: #None or empty
           raise ValueError("Predictions array is empty or None")
       
       if len(predictions) != 10:  #(0-9) we need 10 prediction
           raise ValueError(f"Predictions array should have 10 elements, got {len(predictions)}")
    
       fig, ax = plt.subplots(figsize=(10, 4))
    
       # Make a graph
       labels = [f"{i}" for i in range(10)]
       ax.bar(labels, predictions*100, color='blue')
       ax.set_title("Predicted number: " + str(np.argmax(predictions)))
       ax.set_ylabel("Probability %")
       ax.set_xlabel("Numbers")
       bars = ax.bar(labels, predictions*100)
       
        # show predict munbers top of the column
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
    
        # Save to base64 using the new function
       img_data = save_to_base64(fig)
        # close plot
       plt.close(fig)
    except ValueError as e:
        print(e)
        
    except Exception as e:
        print("Error in create a graph with predictions numbers", e)
    
    return img_data


"""
Get the graph
Save a graph to base64 format
Retun base64 format image
"""
def save_to_base64(fig):
    
    try:
        if fig is None:
            raise ValueError("No image to save. Fig value is None")
        
        # Save to BytesIO png
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png',  bbox_inches='tight')
        img_buf.seek(0)
        
        # Convert to base64
        img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
        
        # Close plot
        plt.close(fig)

    except ValueError as e:
        print(e)
        
    except Exception as e:
        print("Failed to encode image to base64", e)
        
    return f"data:image/png;base64,{img_base64}"


"""
Layer Vilsualisation
Make a new modell(copy) to access layers input and outputs data
Call visualize_feature_maps
"""
def layer_visualization(processed_image):
    try: 
        if preprocess_image is None:
            raise ValueError("No image to predict and visualization")
        if model is None:
            raise ValueError("No modell to image perdiction")
        
        # Create an input layer
        input_tensor = tf.keras.layers.Input(shape=(28, 28, 1))

        # Select a layer (e.g., the first convolutional layer)
        layer_index = 0  # Change this index for different layers

        # Extract the layer
        layer = model.layers[layer_index]
        print(f"Layer name: {layer.name}, type: {type(layer).__name__}")

        # Create a new model that works with the new input and the output of the selected layer
        x = input_tensor
        for i in range(layer_index + 1):
            x = model.layers[i](x)
        
        one_layer_model = tf.keras.Model(inputs=input_tensor, outputs=x)

        # Create a model from scratch for visualization
        input_shape = (28, 28, 1)  # Typical MNIST size
        inputs = tf.keras.layers.Input(shape=input_shape)
        
        # Add layers
        x = inputs
        outputs = []

        # Number of layers to visualize
        num_layers_to_visualize = 8  # E.g., first 5 layers

        for i in range(min(num_layers_to_visualize, len(model.layers))): # max nummber of the modell layer
            layer = model.layers[i] # get the modell i. layer
            x = layer(x) # this layer get a inputs
            outputs.append(x) #add to output list

        # Create the model
        extended_model = tf.keras.Model(inputs=inputs, outputs=outputs)

        # Use with an actual image
        more_feature_maps = extended_model.predict(processed_image)

        # Visualize the results
        layer_names = [model.layers[i].name for i in range(min(num_layers_to_visualize, len(model.layers)))]
        visualize_feature_maps(more_feature_maps, layer_names)
    except ValueError as e:
        print(e)
        
    except Exception as e:
        print("Error loading visual model", e)
        

"""
Layers Vilsualisation (feature maps)
Make graphs with each layer feature maps and save all to layers_images = [] (base64 format)
"""
def visualize_feature_maps(feature_maps, layer_names):
    try:
        if feature_maps and layer_names is None:
            raise ValueError("Missing input value for visualization")
        
        for i, feature_map in enumerate(feature_maps):
            print(f"Layer {i} ({layer_names[i]}) feature map shape: {feature_map.shape}")
            
            #Only the feature maps of the first image are visualized (batch size = 1)
            fmap = feature_map[0]
            
            #Define the display grid
            n_features = fmap.shape[-1]  # Number of channels. fmap.shape activacion map dimension (height, width, num_channels)
            grid_size = int(np.ceil(np.sqrt(n_features))) # We need a 2D grid. The square root of the number of channels (filters).  # This will give you the approximate side length of the grid. np.ceil(Round up if 32 cannel 5.66- 6)
            
            
            # Create a grid to display feature maps (width, height)
            fig = plt.figure(figsize=(15, 15))
            
            # Displays the first few feature maps (max 32 or as much as we request)
            max_features = min(32, n_features)
            for j in range(max_features):
                plt.subplot(grid_size, grid_size, j+1)
                
                # Normalize for better visualization
                img = fmap[:, :, j] #get the featuremap datas (height, width, num_channels)
                img = (img - img.min()) / (img.max() - img.min() + 1e-8)  # Avoid dividing by zero map values should be between 0 and 1
                
                plt.imshow(img, cmap='viridis')
                plt.title(f'Feature {j+1}')
                plt.axis('off')
            
            plt.suptitle(f"Feature Maps from Layer {layer_names[i]}", fontsize=16)
            plt.tight_layout()
            #save graphs to array  (base64) format
            layers_images.append(save_to_base64(fig))
            
    except ValueError as e:
        print(e)
    except Exception as e:   
        print("Error while visualizing feature maps", e)
    