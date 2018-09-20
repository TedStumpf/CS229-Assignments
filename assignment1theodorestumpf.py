#!/usr/bin/python3

# Accessing the Twitter API
# This script describes the basic methodology for accessing a Twitter feed
# or something similar.

# Loading libraries needed for authentication and requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import json


def main():
  # In order to use this script, you must:
  # - Have a Twitter account and create an app
  # - Store in keys.json a property called "twitter" whose value is an
  #     object with two keys, "key" and "secret"
  with open('keys.json', 'r') as f:
     keys = json.loads(f.read())['twitter']

  twitter_key = keys['key']
  twitter_secret = keys['secret']

  # We authenticate ourselves with the above credentials
  # We will demystify this process later
  #
  # For documentation, see http://requests-oauthlib.readthedocs.io/en/latest/api.html
  # and http://docs.python-requests.org/en/master/
  client = BackendApplicationClient(client_id=twitter_key)
  oauth = OAuth2Session(client=client)
  token = oauth.fetch_token(token_url='https://api.twitter.com/oauth2/token',
                            client_id=twitter_key,
                            client_secret=twitter_secret)

  # Base url needed for all subsequent queries
  base_url = 'https://api.twitter.com/1.1/'

  # Particular page requested. The specific query string will be
  # appended to that.
  page = 'search/tweets.json'

  # Depending on the query we are interested in, we append the necessary string
  # As you read through the twitter API, you'll find more possibilities
  req_url = base_url + page + '?q=Hanover+College&tweet_mode=extended&count=100'

  # We perform a request. Contains standard HTTP information
  response = oauth.get(req_url)

  # Read the query results
  results = json.loads(response.content.decode('utf-8'))

  ## Process the results
  ## CAUTION: The following code will attempt to read up to 10000 tweets that
  ## Mention Hanover College. You should NOT change this code.
  tweets = results['statuses']
  while True:
     if not ('next_results' in results['search_metadata']):
        break
     if len(tweets) > 10000:
        break
     next_search = base_url + page + results['search_metadata']['next_results'] + '&tweet_mode=extended'
     print(results['search_metadata']['next_results'])
     response = oauth.get(next_search)
     results = json.loads(response.content.decode('utf-8'))
     tweets.extend(results['statuses'])

  ## CAUTION: For the rest of this assignment, the list "tweets" contains all the
  ## tweets you would want to work with. Do NOT change the list or the value of "tweets".
  print("Found", len(tweets), "tweets")

  # 1
  tweets_text = [get_full_text(tweet) for tweet in tweets]
  # 3
  tags_per_tweet = [get_hashtag_list(tweet) for tweet in tweets]
  # 6
  tagless_tweets = [tweets[i] for i in range(len(tweets)) if tags_per_tweet[i] == []]

  # 4
  hashtags = {}
  for tweet in tags_per_tweet:
    for tag in tweet:
      if tag in hashtags:
        hashtags[tag] += 1
      else:
        hashtags[tag] = 1

  # 7
  orig_tweets = [tweet for tweet in tweets if not 'retweeted_status' in tweet]
  tag_info = {}
  for tag in hashtags:
    tag_dict = {}
    tag_dict['count'] = hashtags[tag]
    tag_dict['percent'] = hashtags[tag] / len(tweets)
    tag_dict['users'] = []
    tag_dict['other_tags'] = []
    
    for tweet in orig_tweets:
      loc_tags = get_hashtag_list(tweet)
      if tag in loc_tags:
        name = tweet['user']['screen_name']
        if not name in tag_dict['users']:
          tag_dict['users'].append(name)

        for other_tag in loc_tags:
          if other_tag != tag and not other_tag in tag_dict['other_tags']:
            tag_dict['other_tags'].append(other_tag)
    tag_info[tag] = tag_dict

  # 8
  with open('tag_info.json', 'w') as f:
    json.dump(tag_info, f)

  # 9
  simpler_tweets = []
  for tweet in tweets:
    simple = {}
    simple['text'] = get_full_text(tweet)
    simple['author'] = tweet['user']['screen_name']
    simple['date'] = tweet['created_at']
    simple['hashtags'] = get_hashtag_list(tweet)
    simple['mentions'] = [user['screen_name'] for user in tweet['entities']['user_mentions']]
    simpler_tweets.append(simple)
  with open('simpler_tweets.json', 'w') as f:
    json.dump(simpler_tweets, f)

  # 5
  print_common_hastags(hashtags, 6)


# 2
def get_full_text(tweet):
  if 'retweeted_status' in tweet:
    return tweet['retweeted_status']['full_text']
  return tweet['full_text']

def get_hashtag_list(tweet):
  tags = []
  for tag_dict in tweet['entities']['hashtags']:
    tag = tag_dict['text'].lower()
    if not tag in tags:
      tags.append(tag)
  return tags

# 5
def print_common_hastags(hashtags, number):
  if (number == -1):
    number = len(hashtags)
  pairs = list(hashtags.items())
  pairs.sort(key = lambda pair: pair[1], reverse = True)
  for i in range(min(number, len(hashtags))):
    print(pairs[i][1], "-", pairs[i][0])


main()