import tweepy  # Need tweepy for REST API to access user followers.

def authentication(filename, stream = False,  wait_on_rate_limit = False, wait_on_rate_limit_notify = False, compression = False):
    # Getting Keys from file.
    key_dictionary = {'consumer_key':'', 'consumer_secret':'', 'access_token':'', 'access_token_secret': ''}
    for line in open(filename,'r'):  # Line-wise iteration.
        key = line.strip().split(' ')  # Split string based on spaces.
        try:
            key_dictionary.update({key[0]:key[1]})
        except KeyError:  # Ignore key error
            pass
        except IndexError:  # Ignore index error
            pass

    # OAuth process, using the keys and tokens.
    auth = tweepy.OAuthHandler(key_dictionary['consumer_key'],key_dictionary['consumer_secret'])
    auth.set_access_token(key_dictionary['access_token'], key_dictionary['access_token_secret'])
    return auth if stream else tweepy.API(auth, wait_on_rate_limit = wait_on_rate_limit, wait_on_rate_limit_notify = wait_on_rate_limit_notify, compression = compression)
