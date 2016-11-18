import networkx as nx  # Making the graph.
import matplotlib.pyplot as plt  #Plotting the graph.
import json  # Tweets in JSON Format.
import tweepy  # Need tweepy for REST API to access user followers.
import re  # Regex required to calculate retweets.
import Authentication  #

#Statistical variables.
tweet_count = 0  # Counter for tweets.
rt_count = 0  # Counter for RTs.
mention_count = 0  # Counter for Mentions.

def draw_Graph(G):
    # Drawing the graphs.
    # Can select any graph and change parameters to add extra features, comment the rest.
    nx.draw(G)
    plt.savefig("draw.png")

    nx.draw_random(G)
    plt.savefig("drawrandom.png")

    nx.draw_spectral(G)
    plt.savefig("drawspectral.png")

    nx.draw_circular(G)
    plt.savefig("drawcircular.png")


def degree_centrality(G):
    # Calculating Degree Centrality.
    centrality_list = nx.degree_centrality(G)
    max_centrality = -1.0
    user_screen_name = ""

    for node in G.nodes():
        if max_centrality < centrality_list[node]:
            max_centrality = centrality_list[node]
            user_screen_name = node

    print("Maximum degree centrality is for user: " + user_screen_name + " (%f)" % max_centrality)

def eigenvector_centrality(G):
    # Calculating Eigenvector Centrality.
    centrality_list = nx.eigenvector_centrality(G)
    max_centrality = -1.0
    user_screen_name = ""

    for node in G.nodes():
        if max_centrality < centrality_list[node]:
            max_centrality = centrality_list[node]
            user_screen_name = node

    print("Maximum eigenvector centrality is for user: " + user_screen_name + " (%f)" % max_centrality)

def betweenness_centrality(G):
    # Calculating Betweenness Centrality.
    centrality_list = nx.betweenness_centrality(G)
    max_centrality = -1.0
    user_screen_name = ""

    for node in G.nodes():
        if max_centrality < centrality_list[node]:
            max_centrality = centrality_list[node]
            user_screen_name = node

    print("Maximum eigenvector centrality is for user: " + user_screen_name + " (%f)" % max_centrality)

def pagerank(G):
    # Calculating Pagerank.
    centrality_list = nx.pagerank(G)
    max_centrality = -1.0
    user_screen_name = ""

    for node in G.nodes():
        if max_centrality < centrality_list[node]:
            max_centrality = centrality_list[node]
            user_screen_name = node

    print("Maximum pagerank is for user: " + user_screen_name + " (%f)" % max_centrality)

def retweet_relation(G, tweet):
    global tweet_count
    global rt_count
    rt_regex = "^(RT )@([A-Za-z0-9]+)\:.*$"  # Regex for RTs.
    user_screen_name = tweet['user']['screen_name']  # Get user_screen_name of the tweeter.

    # Add the user to the graph if not already present.
    tweet_count += 1  # Tweet counter incremented due to valid tweet.
    G.add_node(user_screen_name)  # Populating the graph with nodes.

    # For some reason, retweeted_status doesnt work here, so I'm using regex to extract tweets that are RTs.
    matcher = re.match(rt_regex, tweet['text'])  # Match the text with the Regex for RT.
    if matcher:  # If Regex matches, it is a retweet.
        rt_count += 1  # Increment the counter for retweets.
        G.add_edge(user_screen_name, matcher.group(2))  # Populating the graph with nodes.

    return G

def mention_relation(G, tweet):
    global tweet_count
    global mention_count

    user_screen_name = tweet['user']['screen_name']  # Get user_screen_name of the tweeter.
    user_mentions = tweet['entities']['user_mentions']  # Get entities' JSON Object.
    for user in user_mentions:  # For every user mentioned, add to graph and create edge.
        G.add_edge(user_screen_name,user['screen_name'])

    return G

def followers_ids(tweet):
    user_screen_name = tweet['user']['screen_name']
    # Authentication.
    api = Authentication.authentication('Authentication.txt', wait_on_rate_limit = True, wait_on_rate_limit_notify = True, compression = True)
    cursor = tweepy.Cursor(api.followers_ids, screen_name = user_screen_name)  # Cursor for followers

    ids = []
    for page in cursor.pages():  # For each page in cursor.
        ids.append(page)    # Add page to id.
    pass

    return ids

def main():
    # Creation of the actual interface, using authentication.
    global tweet_count
    global rt_count
    G = nx.DiGraph()  # Creating a Directed Graph.

    # Retrieving all tweets from date.json.
    with open('data.txt', 'r') as f:  # Opening fie.
        line = f.readline()  # Read only the first tweet/line.
        while (line):
            # Try except block to create JSON objects. File doesn't store complete objects, hence have to create them.
            try:  # Tries to load the string as a python dict. If not complete JSON obj, then throws exception.
                tweet_str = line.strip()  # Removing white spaces fom the string.
                tweet = json.loads(tweet_str)  # Load it as Python dict.

                # If it loads the JSON object correctly,
                G = retweet_relation(G, tweet) # Checking and updating graph for retweet relation.
                G = mention_relation(G, tweet) # Checking and updating graph for mentions relation.
                #ids = follower_ids(tweet) # Gets followers of the user. Can get up to 100 pages per 15 mins.

                line = f.readline()  # Retrieves next line from file.

            except ValueError: # If line was not complete JSON boject, append the next line to it.
                line += f.readline()  # Appends next line to the incomplete JSON object.

            except:
                # Ignore all exceptions to check new line. Not a safe practice but I am trusting the data set.
                line = f.readline()  # Retrieves next line from file.
    f.close()

    # Data Statistics.
    print ("Total Nodes: %d" %G.number_of_nodes())  # Printing the total nodes in graph.
    print ("Total Edges: %d" %G.number_of_edges())  # Printing the total nodes in graph.
    print ("Total Tweets: %d" %tweet_count)  # Printing the total tweets in the File.
    print ("Total Retweets: %d" %rt_count)  # Printing the total tweets in the File.

    degree_centrality(G)  # Calculating the degree centrality.
    eigenvector_centrality(G)  # Calculating the eigenvector centrality.
    pagerank(G)  # Calculating the pagerank.
    #betweenness_centrality(G)  # Calculating the betweenness centrality.


if __name__ == '__main__':
    main()