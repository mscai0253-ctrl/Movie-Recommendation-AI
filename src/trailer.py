import requests

API_KEY = "AIzaSyD7LQJhnweMlLD8EIsEUx7IJfCb2249rkM"

def get_trailer(movie):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={movie} trailer&type=video&key={API_KEY}"
        data = requests.get(url).json()

        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["id"]["videoId"]
    except:
        pass

    return None