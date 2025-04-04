#terminal
#run flask server : flask --app server --debug run just development 
#run the server: python server.py (terminal)
# curl.exe http://localhost:5000 , Invoke-WebRequest -Uri http://localhost:5000

#Import Flask
from flask import Flask
from flask import Flask, render_template, request, jsonify, abort
from digit_recognition.model import predict_digit
import numpy as np
import base64
import re
from io import BytesIO
import logging

#create an instance of the Flask class
app = Flask("Digit Recognition")

# Make the error logging file
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#run the index page
@app.route("/") #decorator
def render_index_page():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Can't find the index page: {e}")
        abort(404)  

@app.route("/predict", methods=['POST'])
def img_route():
    try:
        # Retrieve the img to preprocess
        data = request.get_json()
        
        # data is not null and image
        if not data or 'image' not in data:
            app.logger.error("Missing image data")
            return jsonify(error="Missing image data"), 400  # Bad Request
            
        image_data = data['image']
        # Base64 clean
        image_data = re.sub('^data:image/.+;base64,', '', image_data)
        
        # convert image data to base64
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            app.logger.error(f"Error during base64 decoding: {e}")
            return jsonify(error="Incorrect image format"), 400
            
        # BytesIO obj
        image_to_preprocess = BytesIO(image_bytes)
        
        # Pass the image to the prepocess image and predict image function and store the response
        response = predict_digit(image_to_preprocess)
        
        # Check if the answer is of the right length. Response length (5), featuremap images (8) or no response
        if not response or len(response) < 5 or len(response[4]) < 8:
            app.logger.error("Inadequate response length")
            return jsonify(error="Inadequate response length"), 500
        
        #get layers_images array from response
        layers_images = response[4]
        
        return jsonify(prediction = int(response[0]),                     #prediction datas
                       confidence = float(response[1]),
                       visualisation = str(response[2]),
                       greyscaleImage = str(response[3]),
                       firstLayerConv2d = str(layers_images[0]),          #layers images
                       secondLayerMaxPool2d = str(layers_images[1]),
                       thirdLayerConv2d = str(layers_images[2]),
                       fourthLayerConv2d = str(layers_images[3]),
                       fifthLayerMaxPool2d = str(layers_images[4]),
                       sixthLayerConv2d = str(layers_images[5]),
                       seventhLayerConv2d = str(layers_images[6]),
                       eighthLayerMaxPool2d = str(layers_images[7]))
                       
    except Exception as e:
        app.logger.error(f"Error on recognition: {e}")
        return jsonify(error="Server error"), 500

# 404 (Not Found) 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500 (Server Error) 
@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Error 500: {e}")
    return render_template('500.html'), 500

# Test 500 rute
@app.route('/test-500')
def test_500():
    abort(500)

#host and run the server
if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000)
    app.run(host="127.0.0.1", port=5000, debug=True) #localhost
   
