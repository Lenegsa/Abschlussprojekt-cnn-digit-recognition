#run flask server : flask --app server --debug run just development
#run the server: python server.py 
# curl.exe http://localhost:5000 , Invoke-WebRequest -Uri http://localhost:5000

#Import Flask
from flask import Flask
from flask import Flask, render_template, request

#create an instance of the Flask class
app = Flask(__name__)

#run the index page
@app.route("/")
def render_index_page():
    return render_template('index.html')



#host and run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


#if __name__ == "__main__":
    #enable debug mode
    #app.run(debug=True)
    