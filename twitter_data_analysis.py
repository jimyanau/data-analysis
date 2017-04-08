from tweepy import OAuthHandler, Stream			#import handler
from tweepy.streaming import StreamListener		#import a class

consumer_key = 'whndeJiLln26BoRNeavlLSPoF'
consumer_secret = 'Kaw6qo7EwyWtC0ZSVQCYJ28GjAetH6EUMZGSCHWWgHp4nic8EN'
access_token = '50491256-C47HUO0RRLCGVBFxkVsIY3tw9oEYKaEmdJchLxV1t'
access_token_secret = 'GwZlGWMb9YfstC2w5XLio79i4GQu0rALvnV85zSEW6fpT'

auth = OAuthHandler(consumer_key,
					consumer_secret)		#instance

auth.set_access_token(access_token, access_token_secret)		#call set_access_token function

#Create your own class from class StreamListener
class PrintListener(StreamListener):
	#create method
	def on_status(self, status):
		if not status.text[:3] == 'RT ':	#do not select the re-twitts, which the first 3 chars are 'RT '
			print(status.text)
			print(status.author.screen_name, 
				  status,
				  created_at, 
				  status.source, 
				  '\n')

	def on_error(self,status_code):
		print("Error code: {}".format(status_code))
		return True # keep stream alive

	def on_timeout(self):
		print('Listener timed out!')
		return True # keep stream alive

def print_to_terminal():
	listener = PrintListener()
	stream = Stream(auth, listener)
	languages = ('en',)
	stream.sample(languages=languages)

# tell Python to run the code as script
if __name__ == '__main__':
	print_to_terminal()