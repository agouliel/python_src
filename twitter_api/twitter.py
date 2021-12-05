# Joel Grus book

from twython import Twython
import os

CONSUMER_KEY = os.environ['T_CONS_KEY']
CONSUMER_SECRET = os.environ['T_CONS_SECRET']
ACCESS_TOKEN = os.environ['T_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['T_ACCESS_TOKEN_SECRET']

twitter_client = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

for status in twitter_client.search(q='"data science"')["statuses"]:
    user = status["user"]["screen_name"]
    text = status["text"]
    print(f"{user}: {text}\n")
