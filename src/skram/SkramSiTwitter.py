import sys, math
from django.conf import settings
from urllib2 import HTTPError
from oauth import OAuthToken
from oauthtwitter import OAuthApi
import twitter

def format_tweet_date(tweet):
    '''Get a human redable string representing the posting time

    Returns:
      A human readable string representing the posting time
    '''
    fudge = 1.25
    delta  = float(tweet.now) - float(tweet.created_at_in_seconds)
    
    delta_formats = (
        {'span':60, 'format_str':'pred %d %s', 'time_forms':('sekundo', 'sekundama', 'sekundami')},
        {'span':60, 'format_str':'pred %d %s', 'time_forms':('minuto', 'minutama', 'minutami')},
        {'span':24, 'format_str':'pred %d %s', 'time_forms':('uro', 'urama', 'urami')},
        {'span':sys.maxint, 'format_str':'pred %d %s', 'time_forms':('dnevom', 'dnevoma', 'dnevi')})

    for delta_format in delta_formats:
           
        if delta < fudge:
            return delta_format['format_str'] % (1, delta_format['time_forms'][0])
        elif delta < (fudge + 1):
            return delta_format['format_str'] % (2, delta_format['time_forms'][1])
        elif delta < (delta_format['span'] * (1/fudge)):
            return delta_format['format_str'] % (math.ceil(delta), delta_format['time_forms'][2])
        
        delta = delta / delta_format['span']
        
    raise Exception, "Out of delta range exception."


def get_twitterAPI():
    access_token = OAuthToken(settings.TWITTER_SKRAMSI_KEY, settings.TWITTER_SKRAMSI_SECRET)
    return OAuthApi(settings.TWITTER_SKRAMSI_CONSUMER_KEY, settings.TWITTER_SKRAMSI_CONSUMER_SECRET, access_token)
    
    
def get_latest_tweets():
    
    try:
        twitterAPI = get_twitterAPI()
        tweets = twitterAPI.GetUserTimeline(settings.TWITTER_USER, settings.TWITTER_TWEETS_SHOWN)
    except HTTPError, e:
        raise twitter.TwitterError('Twitter is not available. HTTPError: ' + str(e))
    
    for tweet in tweets:
        tweet.date_str = format_tweet_date(tweet)
        
    return tweets

def post_status_update(status):
    twitterAPI = get_twitterAPI()
    twitterAPI.PostUpdate(status)
    