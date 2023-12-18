import requests
import json


class ConvertSpofity:
    # TODO: Add error handling
    def __init__(self, spotify_url):
        with open("config.json", "r") as f:
            config = json.load(f)
            self.client_secret = config["spotify_client_secret"]
            self.client_id = config["spotify_client_id"]
            self.google_api_key = config["google_api_key"]
            self.spotify_url = spotify_url

    def get_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(url, headers=headers, data=data)
        return response.json()["access_token"]

    def get_song_obj(self, spotify_url):
        artist_obj = {}
        song_id = spotify_url.split("/")[-1]

        headers = {"Authorization": f"Bearer {self.get_token()}"}
        response = requests.get(
            f"https://api.spotify.com/v1/tracks/{song_id}", headers=headers
        )
        data = response.json()

        artist_names = [artist["name"] for artist in data["artists"]]

        return {
            "track_name": data["name"],
            "artist_names": artist_names,
        }

    def get_youtube_url(self):
        song = self.get_song_obj(self.spotify_url)
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={str(song['artist_names'])}%20{song['track_name']}&type=video&key={self.google_api_key}"
        yt = requests.get(url=url).json()
        video_id = yt["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
