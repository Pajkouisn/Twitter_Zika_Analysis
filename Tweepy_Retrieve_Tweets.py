import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import time
import Authentication

auth = Authentication.authentication('Authentication_Fex.txt', stream=True)

'''
#tweepy REST API.
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
# Sample method, used to update a status
 api.update_status('Using Tweepy!')
'''

#tweepy Stream API.
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open(time.strftime("%d%B%Y.json"), 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print(str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['Zika'])