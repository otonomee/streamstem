import requests
import json
from base64 import b64decode
from fake_useragent import UserAgent


class Downloader:
    def __init__(self):
        self.zyte_api_key = "da91cf171873419d90bf6ae752409a57"
        self.ua = UserAgent()
        self.session = requests.Session()

    def __request_zyte_api(self, url):
        payload = {
            "url": url,
            # "browserHtml": True,
            # "httpResponseBody": True,
            # "httpResponseHeaders": True,
            # "javascript": True,
            "customHttpRequestHeaders": {
                "User-Agent": self.ua.random,
            },
        }

        try:
            api_response = self.session.post(
                "https://api.zyte.com/v1/extract",
                auth=(self.zyte_api_key, ""),
                json=payload,
            )
            api_response.raise_for_status()

            response_json = api_response.json()
            if "httpResponseBody" in response_json:
                return b64decode(response_json["httpResponseBody"]).decode("utf-8")
            else:
                print("No httpResponseBody in the API response.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error in Zyte API request: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.text}")
            return None

    def download_video(self, youtube_url, filetype):
        # We'll use youtube-dl's extract_info functionality
        extract_url = f"https://youtube-dl.org/api/info?url={youtube_url}"
        response_body = self.__request_zyte_api(extract_url)

        if response_body:
            video_info = json.loads(response_body)
            if "title" in video_info:
                filename = f"{video_info['title']}.{filetype}"
                # Here you would typically download the audio
                # For this example, we'll just return the filename
                return filename
            else:
                print("Failed to extract video information")
                return None
        else:
            print("Failed to get response from Zyte API")
            return None

    def get_video_info(self, youtube_url):
        extract_url = f"https://youtube-dl.org/api/info?url={youtube_url}"
        response_body = self.__request_zyte_api(extract_url)

        if response_body:
            return json.loads(response_body)
        else:
            print("Failed to get video info from Zyte API")
            return None


# Usage example:
# downloader = Downloader(zyte_api_key="your_zyte_api_key_here")
# filename = downloader.download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "mp3")
# video_info = downloader.get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
