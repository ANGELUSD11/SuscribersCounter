from flask import Flask, render_template
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_subscriber_count():
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "statistics",
        "id": CHANNEL_ID,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    try:
        return int(data["items"][0]["statistics"]["subscriberCount"])
    except (KeyError, IndexError):
        return None
    
@app.route('/', methods=['GET'])
def index():
    suscribers_count = get_subscriber_count()
    return render_template('index.html', suscribers_count=suscribers_count)

def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)