import requests

res = requests.post('http://localhost:8000/puddlr.com/files/create',
                    files={'file': open('hearthstone-7level.png', 'rb')})

print(res.text)