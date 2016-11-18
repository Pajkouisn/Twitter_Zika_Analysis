from twitter import *
from twitter import Twitter

import json

#Access token for my app on twitter.
Access_token = ''
Access_secret = ''
API_key = ''
API_secret = ''

oauth = OAuth(Access_token, Access_secret, API_key, API_secret)

twitter = Twitter(auth=oauth)
twitter_stream = TwitterStream(auth=oauth)
# Initiate the connection to Twitter Streaming API

iterator = twitter_stream.statuses.filter(track="Zika", language = "en",locations = '-122.75,36.8,-121.75,37.8')
#locations = "-80,25,-88,30"
tweet_count = 10
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    # print json.dumps(tweet)
    # The command below will do pretty printing for JSON data, try it out
    print json.dumps(tweet, indent=4)

    if tweet_count <= 0:
        break