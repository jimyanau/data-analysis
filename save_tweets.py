import json
from os import path

from tweepy import OAuthoHandler, Stream
from tweepy.streaming import StreamListener

from sqlalchemy.orm.exc import NoResultFound

from data_analysis.database import session Tweet, Hashtag, User

consumer_key = 'whndeJiLln26BoRNeavlLSPoF'
consumer_secret = 'Kaw6qo7EwyWtC0ZSVQCYJ28GjAetH6EUMZGSCHWWgHp4nic8EN'
access_token = '50491256-C47HUO0RRLCGVBFxkVsIY3tw9oEYKaEmdJchLxV1t'
access_token_secret = 'GwZlGWMb9YfstC2w5XLio79i4GQu0rALvnV85zSEW6fpT'

auth = OAuthHandler(consumer_key,
					consumer_secret)		#instance

auth.set_access_token(access_token, access_token_secret)		#call set_access_token function

def save_tweets():
	directory = _get_dir_absolute_path()
	filepath = path.join(directory, 'tweets.json')

	listener = DatabaseListener(number_tweets_to_save = 1000,
								filepath = filepath)
	stream = tweepy.Stream(auth, listener)
	languages = ('en',)
	try:
		stream.sample(languages=languages)
	except KeyboardInterrupt:
		listener.file.close()

