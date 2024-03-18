#!/usr/bin/env python3
from flask import Flask, render_template, request
from googleapiclient.discovery import build

app = Flask(__name__)

@app.route('/', strict_slashes=False)
@app.route('/Home', strict_slashes=False)
def index():
    #return "<h1>Hello World!<h1>"
    return render_template('index.html')

@app.route('/index/search', methods=['GET', 'POST'], strict_slashes=False)
def search():
    from googleapiclient.discovery import build  # Add this import statement
    api_key = "AIzaSyAaUOV1XCdm7hGf_Z4Gns9eFmAJva8HBqc"  # Replace with your actual API key
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    video_info = []
    if request.method == 'POST':
        try:
            search_query = request.form.get('query')
            response = youtube.search().list(
                q=search_query,
                part='snippet',
                type='video',
                maxResults=10
            ).execute()

            for item in response.get('items', []):
                title = item.get('snippet', {}).get('title', '')
                description = item.get('snippet', {}).get('description', '')
                thumbnails = item.get('snippet', {}).get('thumbnails', {})
                thumbnail_url = thumbnails.get('default', {}).get('url', '')
                video_id = item.get('id', {}).get('videoId', '')
                video_url = f'https://www.youtube.com/embed/{video_id}'
                video_info.append({'title': title, 'description': description, 
                                   'thumbnail': thumbnail_url,
                                   'url': video_url, 'video_id': video_id})
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('search.html', videos=video_info)

    
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')


