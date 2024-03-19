

from flask import Flask, request
import os
from dotenv import load_dotenv
import base64
import json
import requests

load_dotenv()

youtube_api_key = os.getenv('youtubedataapikey')
spotify_client_id = os.getenv('spotifyclientId')
spotify_client_secret = os.getenv('spotifyclientsecret')

def get_token():
    client_id = spotify_client_id
    client_secret = spotify_client_secret
    # Construct the request URL
    token_url = 'https://accounts.spotify.com/api/token'
    
    # Set the request headers
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
    }
    
    # Set the request payload
    payload = {
        'grant_type': 'client_credentials',
    }
    
    # Send the POST request to get the token
    response = requests.post(token_url, headers=headers, data=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        token_data = response.json()
        
        # Extract the access token
        access_token = token_data.get('access_token')
        
        # Return the access token
        return access_token
    else:
        # Return an error message
        return 'Failed to get access token'
def query_youtube():
    from googleapiclient.discovery import build  # Add this import statement
    api_key = "AIzaSyCy5ifWLKdwa_Sq_RuDCBa2bjRr4uucUtU"  # Replace with your actual API key
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
        
    return video_info