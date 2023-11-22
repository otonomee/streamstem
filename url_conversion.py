import requests
import json

class UrlConverter:
    def convert_to_youtube_url(self, source_url):
        with open('api_token.json') as f:
            data = json.load(f)
            api_token = data['api_token']

        url = 'https://api.soundiiz.com/v1/resolve'
        headers = {
            'accept': '*/*',
            'Authorization': api_token
        }

        params = {
            'url': source_url,
            'services': 'ytmusic,deezer,tidal,qobuz,applemusicapp'
        }

        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()
        print(response_data)
        for service in response_data['data']:
            if service['serviceName'] == 'ytmusic':
                return service['trackUrl']
            
