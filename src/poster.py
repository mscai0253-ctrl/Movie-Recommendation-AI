import requests

API_KEY = "339fa195"

def fetch_poster(movie):
    try:
        url = f"http://www.omdbapi.com/?t={movie}&apikey={API_KEY}"
        data = requests.get(url).json()

        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]
    except:
        pass

    return "https://via.placeholder.com/300x450?text=No+Image"