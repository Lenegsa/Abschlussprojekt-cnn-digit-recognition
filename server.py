#run flask server : flask --app server --debug run just development
# curl.exe http://localhost:5000 , Invoke-WebRequest -Uri http://localhost:5000

#Import Flask
from flask import Flask

#create an instance of the Flask class
app = Flask(__name__)

#Define a rute for the root URL ("/")

@app.route("/")
def index():
   return{"message":"Hello World"}



if __name__ == "__main__":
    #enable debug mode
    app.run(debug=True)