#!/usr/bin/env python

# https://github.com/ytdl-org/youtube-dl/issues/28859#issuecomment-957135234
# https://gitlab.com/ewtoombs/footube (full client)

from requests import Session
import json

def api_key(response):
    from bs4 import BeautifulSoup
    import re
    soup = BeautifulSoup(response, 'html.parser')
    key = None
    for script_tag in soup.find_all('script'):
        script = script_tag.string
        if script is not None:
            match = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', script)
            if match is not None:
                key = match.group(1)
                break
    assert key is not None
    return key


id = 'yiw6_JakZFc'

session = Session()
session.headers = {
    # This is to demonstrate how little the user agent matters
    'User-Agent': 'Fuck you, Google!',
}

# Hit the /watch endpoint, but we actually only want an API key lol.
response = session.get(
    'https://www.youtube.com/watch',
    params={'v': id},
).content.decode()
key = api_key(response)

# OK, now use the API key to get the actual streaming data.
post_data = {
    'context': {
        'client': {
            'clientName': 'ANDROID',
            'clientVersion': '16.05',
        },
    },
    'videoId': id,
}
data = json.loads(session.post(
    'https://www.youtube.com/youtubei/v1/player',
    params={'key': key},
    data=json.dumps(post_data),
).content)

for f in data['streamingData']['adaptiveFormats']:
    if 'height' in f and f['height'] == 720:
        print(f['url']+'&range=0-10000000')
        break
