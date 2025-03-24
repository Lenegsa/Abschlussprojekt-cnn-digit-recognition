#terminal
#run flask server : flask --app server --debug run just development 
#run the server: python server.py (terminal)
# curl.exe http://localhost:5000 , Invoke-WebRequest -Uri http://localhost:5000

#Import Flask
from flask import Flask
from flask import Flask, render_template, request, jsonify
from models.model import preprocess_image, predict_digit
import base64
import re
from io import BytesIO

#create an instance of the Flask class
app = Flask("Digit Recognition")

#run the index page
@app.route("/") #decorator
def render_index_page():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def img_route():
     # Retrieve the img to preprocess 
    data = request.get_json()
    image_data = data['image']
     # Base64 clean
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_bytes  = base64.b64decode(image_data)
      # BytesIO obj
    image_to_preprocess = BytesIO(image_bytes)
    
    # Pass the image to the prepocess image and predict image function and store the response
    response = predict_digit(image_to_preprocess)
    digit = response[0]
    
    return jsonify({'prediction': int(digit)})
    


#host and run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


#if __name__ == "__main__":
    #enable debug mode
    #app.run(debug=True)
    