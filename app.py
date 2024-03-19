# Description: This file is the main file for the Flask application. It will handle the routing and rendering of the web pages.
from flask import Flask, render_template, request
from googleapiclient.discovery import build
from model import *

app = Flask(__name__)

@app.route('/', strict_slashes=False)
@app.route('/Home', strict_slashes=False)
def index():
    #return "<h1>Hello World!<h1>"
    return render_template('index.html')

@app.route('/index/search', methods=['GET', 'POST'], strict_slashes=False)
def search():
    video_info = query_youtube()

    return render_template('search.html', videos=video_info)

    
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')


