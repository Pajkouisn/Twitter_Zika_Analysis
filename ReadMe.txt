
Install all the packages required: 
	tweepy/twitter
	matplotlib
	networkx

Files:
	Python_Twitter_searchAPI.py
	Authentication.py
	Tweepy_Retrieve_Tweets.py
	Analyzing_Data_Set.py

Steps:

To collect tweets, run Tweepy_Retrieve_Tweets.py. 
To analyze tweets, run Analyzing_Data_Set.py by adding the filename of the file to be analyzed. 

In both cases, set your consumer and authentication keys in the Authentication.txt file. Authentication.py reads the keys from this file to perform authentication and establish a connection. The data in the Authentication.txt file should be in the following format:

consumer_key <enter__your_consumer_key_here>
consumer_secret <enter_your_consumer_secret_here>
access_token <enter_your_access_token_here>
access_token_secret <enter_your_access_token_secret_here>

For streaming, ensure that you pass the stream = True parameter to the Authentication.authentication function, because the default value will be False which is for hte Rest api.

Algorithm and File Descriptions:

Python_Twitter_searchAPI.py:
First I tried to use the python twitter API (Python_Twitter_searchAPI.py), but I ran into many problems. When collecting tweets, if the TCP connection with the application breaks, then the iterator yields a {'hangup': True} and raises `StopIteration` if iterated again. Hence, if the program isn't fast enough, it will break the connection, meaning that analyzing the data being retrieved is hectic. Similarly, if the stream does not produce tweets (or heartbeats) for more than 90 seconds, the iterator yields `{'hangup': True,'heartbeat_timeout': True}`, and raises `StopIteration` if iterated again. So to summarize, if the stream produces tweets too fast (say if searching for keyword 'and') or too slow (as in this case where 'Zika' is being searched), the connection breaks.

Tweepy_Retrieve_Tweets.py:
Having scrapped the use of python twitter API (Tweepy_Retrieve_Tweets.py), I moved to tweepy. In tweepy, I used the stream API to continuously get tweets about Zika. These are stored in a file that is determined by the current date. If today is 03/05/2016, it stores the data in the file 05March2016. 

Authentication.py:
This file essentially authenticates and creates the actual interface for retrieving tweets from twitter. I has customizable parameters to switch between stream API (stream = true) or REST API (stream = false). It also accepts parameters (retry_count, wait_on_rate_limit, wait_on_rate_limit_notify, compression) for the REST API. Retry_count is the default number of times to retry when an error occurs. Wait_on_rate_limit_notify and wait_on_rate_limit notifies if the rate limit is exceeded and waits the required amount of time (15 minutes the first time that is incremented each time rate_limit is exceeded) before being able to retrieve the next data. Compression parameter is whether or not to use GZIP compression for requests

Analyzing_Data_Set.py:
The file to be analysed is opened in the main() function. the retweet_relation(graph, tweet), mention_relation(graph, tweet) and follower_ids(tweet) are called to build the graphs. Retweet_relation(graph, tweet) function creates the retweet edges in the graph, mention_relation(graph, tweet) created the edges when a person is mentioned in a tweet and follower_ids(tweet) returns the ids of a user's followers. draw_Graph(graph) draws graphs using pyplot from matplotlib, degree_centrality(graph)  is calculating the degree centrality, eigenvector_centrality(graph) is calculating the eigenvector centrality, pagerank(graph) is calculating the page rank and betweenness_centrality(graph) is calculating the betweenness centrality (This takes long).
