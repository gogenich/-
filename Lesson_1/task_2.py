import requests
import json
'''api youtube'''

part_1 = '&part=snippet,contentDetails,statistics,status'
apid = 'AIzaSyATVxQllrPCVPR--u2SZVJ0Fn_M6mpbIAM'
url = f'https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key={apid}{part_1}'

#user agent
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'}
data = requests.get(url, headers=headers).json()
with open('data_youtube.json', 'w') as out:
    json.dump(data, out)
print(data)