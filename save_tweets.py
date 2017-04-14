import json
from os import path

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

from sqlalchemy.orm.exc import NoResultFound

# import method we created in databse.py
from database import session, Tweet, Hashtag, User

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
	stream = Stream(auth, listener)
	languages = ('en',)
	try:
		stream.sample(languages=languages)
	except KeyboardInterrupt:
		listener.file.close()

class DatabaseListener(StreamListener):
	def __init__(self, number_tweets_to_save, filepath=None):
		self._final_count = number_tweets_to_save
		self._current_count = 0
		if filepath is None:
			filepath = 'tweet.txt'
		self.file = open(filepath, 'w')

	# Note: Slightly dangerous due to circular references
	def __del__(self):
		self.file.close()

	# Modify the on_data method
	def on_data(self, raw_data):
		data = json.loads(raw_data)
		json.dump(raw_data, self.file)
		self.file.write('\n')
		if 'in_reply_to_status_id' in data:
			return self.on_status(data)

	def on_status(self, data):
		# Note: This method is defined in this file
		save_to_databse(data)

		self._current_count += 1
		print('Status count: {}'.format(self._current_count))
		if self._current_count >= self._final_count:
			return False

def create_user_helper(user_data):
	# alias to shorten calls
	u = user_data
	user = User(uid=u['id_str'],
				name=u['name'],
				screen_name=u['screen_name'],
				created_at=u['created_at'],
				description=u.get('description'),
				followers_count=u['followers_count'],
				statuses_count=u['statuses_count'],
				favourites_count=u['favourites_count'],
				listed_count=u['listed_count'],
				geo_enabled=u['geo_enabled'],
				lang=u.get('lang'))

	return user


def create_tweet_helper(tweet_data, user):
	# alias to shorten calls
	t = tweet_data
	retweet = True if t['text'][:3] == 'RT ' else False
	coordinates = json.dumps(t['coordinates'])
	tweet = Tweet(tid=t['id_str'],
				  tweet=t['text'],
				  user=user,
				  coordinates=coordinates,
				  create_at=t['created_at'],
				  favorites_count=t['favourite_count'],
				  in_reply_to_screen_name=t['in_reply_to_screen_name'],
				  in_reply_to_status_id=t['in_reply_to_status_id'],
				  in_reply_to_user_id=t['in_reply_to_user_id'],
				  lang=t.get('lang'),
				  quoted_status_id=t.get('quoted_status_id'),
				  retweet_count=t['retweet_count'],
				  source=t['source'],
				  is_retweet=retweet)

	return tweet

def save_to_database(data):
	try:
		user = session.query(User).filter_by(id=str(data['user']['id'])).one()
	except NoResultFound:
		user = create_user_helper(data['user'])
		session.add(user)

	hashtag_results = []

	hashtag = data['entities']['hashtags']
	for hashtag in hashtags:
		hashtag = hashtag['text'].lower()
		try:
			htag = session.query(Hashtag).filter_by(text=hashtag).one()
		except NoResultFound:
			htag = Hashtag(text=hashtag)
			session.add(htag)
		hashtag_results.append(htag)

	tweet = create_tweet_helper(data, user)
	for hashtag in hashtag_results:
		tweet.hashtags.append(hashtag)

	session.add(tweet)
	session.commit()


# search if the user exists, if not, create a new one
def save_to_database(data):
	try:
		user = session.query(User).filter_by(id=str(data['user']['id'])).one()
	except NoResultFound:
		user = create_user_helper(data['user'])
		session.add(user)

	hashtag_results = []
	hashtags = data['entites']['hashtags']
	for hashtag in hashtags:
		hashtag = hashtag['text'].lower()
		try:
			hashtag_obj = session.query(Hashtag).filter_by(text=hashtag).one()
		except NoResultFound:
			hashtag_obj = Hashtag(text=hashtag)
			session.add(hashtag_obj)

		hashtag_results.append(hashtag_obj)

	tweet = create_tweet_helper(data, user)

	# check if the tweet had been added to database
	for hashtag in hashtag_results:
		tweet.hashtags.append(hashtag)

	session.add(tweet)
	session.commit()


def _get_dir_absolute_path():
	"""
	helper method to get the absolute path of the file directory
	"""
	directory = path.abspath(path.dirname(__file__))
	return directory

if __name__ == '__main__':
	save_tweets
