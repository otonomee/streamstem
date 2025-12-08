import requests
import json
import os
from typing import Dict, List


class ConvertSpofity:
    def __init__(self, spotify_url: str):
        """
        Initialize Spotify to YouTube converter.

        Args:
            spotify_url: Spotify track URL

        Raises:
            ValueError: If required environment variables are not set
        """
        # Load credentials from environment variables
        self.client_id = os.environ.get("SPOTIFY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")

        # Validate all required credentials are present
        missing_vars = []
        if not self.client_id:
            missing_vars.append("SPOTIFY_CLIENT_ID")
        if not self.client_secret:
            missing_vars.append("SPOTIFY_CLIENT_SECRET")
        if not self.google_api_key:
            missing_vars.append("GOOGLE_API_KEY")

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                "Please set these in your .env file or environment."
            )

        self.spotify_url = spotify_url

    def get_token(self) -> str:
        """
        Get Spotify API access token.

        Returns:
            str: Access token

        Raises:
            requests.exceptions.RequestException: If API request fails
            ValueError: If response doesn't contain access token
        """
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            token_data = response.json()

            if "access_token" not in token_data:
                raise ValueError("Spotify API response missing access_token")

            return token_data["access_token"]

        except requests.exceptions.Timeout:
            raise requests.exceptions.RequestException(
                "Spotify API request timed out. Please try again."
            )
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise ValueError(
                    "Invalid Spotify credentials. Please check SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET."
                )
            elif response.status_code == 429:
                raise requests.exceptions.RequestException(
                    "Spotify API rate limit exceeded. Please try again later."
                )
            else:
                raise requests.exceptions.RequestException(
                    f"Spotify API error: {response.status_code} - {str(e)}"
                )
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"Failed to connect to Spotify API: {str(e)}"
            )

    def get_song_obj(self, spotify_url: str) -> Dict[str, any]:
        """
        Get track metadata from Spotify.

        Args:
            spotify_url: Spotify track URL

        Returns:
            dict: Track metadata with track_name and artist_names

        Raises:
            ValueError: If URL format is invalid or track not found
            requests.exceptions.RequestException: If API request fails
        """
        try:
            # Extract track ID from URL
            song_id = spotify_url.split("/")[-1].split("?")[0]
            if not song_id or len(song_id) != 22:
                raise ValueError(
                    "Invalid Spotify URL format. Expected format: "
                    "https://open.spotify.com/track/{track_id}"
                )

            # Get track metadata
            headers = {"Authorization": f"Bearer {self.get_token()}"}
            response = requests.get(
                f"https://api.spotify.com/v1/tracks/{song_id}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            # Validate response structure
            if "name" not in data or "artists" not in data:
                raise ValueError("Invalid response from Spotify API")

            artist_names = [artist["name"] for artist in data["artists"]]

            return {
                "track_name": data["name"],
                "artist_names": artist_names,
            }

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"Spotify track not found: {song_id}")
            elif response.status_code == 401:
                raise ValueError("Spotify authentication failed. Check credentials.")
            else:
                raise requests.exceptions.RequestException(
                    f"Spotify API error: {response.status_code}"
                )
        except requests.exceptions.Timeout:
            raise requests.exceptions.RequestException(
                "Spotify API request timed out. Please try again."
            )
        except (KeyError, IndexError) as e:
            raise ValueError(f"Failed to parse Spotify response: {str(e)}")

    def get_youtube_url(self) -> str:
        """
        Convert Spotify track to YouTube URL by searching for matching video.

        Returns:
            str: YouTube video URL

        Raises:
            ValueError: If no matching video found or API response invalid
            requests.exceptions.RequestException: If API request fails
        """
        try:
            song = self.get_song_obj(self.spotify_url)

            # Build search query
            artist_str = " ".join(song['artist_names'])
            search_query = f"{artist_str} {song['track_name']}"

            # Query YouTube API
            url = (
                f"https://www.googleapis.com/youtube/v3/search"
                f"?part=snippet&maxResults=1&q={search_query}"
                f"&type=video&key={self.google_api_key}"
            )

            response = requests.get(url=url, timeout=10)
            response.raise_for_status()
            yt = response.json()

            # Validate response structure
            if "items" not in yt or len(yt["items"]) == 0:
                raise ValueError(
                    f"No YouTube video found for: {search_query}. "
                    "Try a different track or use a YouTube URL directly."
                )

            if "id" not in yt["items"][0] or "videoId" not in yt["items"][0]["id"]:
                raise ValueError("Invalid YouTube API response structure")

            video_id = yt["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"

        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                raise ValueError(
                    "YouTube API quota exceeded or invalid API key. "
                    "Check GOOGLE_API_KEY."
                )
            elif response.status_code == 400:
                raise ValueError(
                    f"Invalid YouTube API request: {response.text}"
                )
            else:
                raise requests.exceptions.RequestException(
                    f"YouTube API error: {response.status_code}"
                )
        except requests.exceptions.Timeout:
            raise requests.exceptions.RequestException(
                "YouTube API request timed out. Please try again."
            )
        except (KeyError, IndexError) as e:
            raise ValueError(f"Failed to parse YouTube response: {str(e)}")
