import logging
from django.core.cache import cache
from django.conf import settings
import twitter
import SkramSiTwitter

def latest_tweets(request):
    tweets = cache.get('tweets')

    if tweets:
        return {"tweets": tweets}
     
    try:
        tweets = SkramSiTwitter.get_latest_tweets() 
    except twitter.TwitterError, e:
        logging.warning('Error accessing latest tweets. ' + str(e))
        return {}

    cache.set('tweets', tweets, settings.TWITTER_TIMEOUT)

    return {"tweets": tweets}

    