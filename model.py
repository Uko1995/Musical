

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
    """get spotify access token"""
    client_id = spotify_client_id
    client_secret = spotify_client_secret
    # Construct the request URL
    token_url = 'https://accounts.spotify.com/api/token'
    
    # Set the request headers
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
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
    
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_artist(token, artist_name):
    url = 'http://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    
def query_youtube():
    from googleapiclient.discovery import build  # Add this import statement
    api_key = "AIzaSyCy5ifWLKdwa_Sq_RuDCBa2bjRr4uucUtU"  # Replace with your actual API key
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    info = []
    if request.method == 'POST':
        try:
            search_query = request.form.get('query')
            search_type = request.form.get('content_type')
            if search_type == 'video':
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
                    info.append({'title': title, 'description': description, 
                                   'thumbnail': thumbnail_url,
                                   'url': video_url, 'video_id': video_id})
            
            elif search_type == 'playlist':
                response = youtube.search().list(
                    q=search_query,
                    part='snippet',
                    type='playlist',
                    maxResults=10
                ).execute()
                for item in response.get('items', []):
                    title = item.get('snippet', {}).get('title', '')
                    description = item.get('snippet', {}).get('description', '')
                    thumbnails = item.get('snippet', {}).get('thumbnails', {})
                    thumbnail_url = thumbnails.get('default', {}).get('url', '')
                    playlist_id = item.get('id', {}).get('playlistId', '')
                    playlist_url = f'https://www.youtube.com/playlist?list={playlist_id}'
                    info.append({'title': title, 'description': description, 
                                   'thumbnail': thumbnail_url,
                                   'url': playlist_url, 'playlist_id': playlist_id})
            elif search_type == 'channel':
                response = youtube.search().list(
                    q=search_query,
                    part='snippet',
                    type='channel',
                    maxResults=10
                ).execute()
                for item in response.get('items', []):
                    title = item.get('snippet', {}).get('title', '')
                    description = item.get('snippet', {}).get('description', '')
                    thumbnails = item.get('snippet', {}).get('thumbnails', {})
                    thumbnail_url = thumbnails.get('default', {}).get('url', '')
                    channel_id = item.get('id', {}).get('channelId', '')
                    channel_url = f'https://www.youtube.com/channel/{channel_id}'
                    info.append({'title': title, 'description': description, 
                                   'thumbnail': thumbnail_url,
                                   'url': channel_url, 'channel_id': channel_id})
            else:
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
                    info.append({'title': title, 'description': description, 
                                   'thumbnail': thumbnail_url,
                                   'url': video_url, 'video_id': video_id})
        
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return info