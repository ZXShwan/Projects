from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features


consumer_key = 'RP3ZNSHdjd0LH0RlMS3rhpSo1'
consumer_secret = 'i78LTPwoIbWs7zn8Do5E2Eb2uZqOTWnW8LUH7WcFk1MyAnNR5b'
access_token = '2509163336-HXCvtWS2pJ4Jo234RjFIh5ii4c8JX71FOPWqE21'
access_token_secret = 'tMf1c9s0guQMU8gKhwJI31bl4EIphfRF5jBmBMxMcZ8q3'


class MyStreamListener(StreamListener):

	def on_status(self, status):
		natural_language_understanding = NaturalLanguageUnderstandingV1(version='2017-02-27',username='c353af43-3172-455f-934a-daa55225e687',password='TLD5MMIRRGIh')
		twitts = status.text
		coordinates = status.coordinates
		language = status.user.lang

		if status.place and language == 'en':
			if coordinates is not None and len(coordinates) > 0:
				coordinates = status.coordinates['coordinates']
				print 'coordinates: ', coordinates

				try:
					response = natural_language_understanding.analyze(
						text=twitts,
						features=[features.Sentiment()]
					)
					sentiment = response['sentiment']['document']['label']
				except Exception as e:
					sentiment = "neutral"
				print sentiment

				upload_data = {
					"twitts": twitts,
					"coordinates": coordinates,
					"sentiment": sentiment
				}
				print requests.post('http://search-trends-jrxihqihqwdzupkozsfp42mqx4.us-east-1.es.amazonaws.com/twittermap/data', json=upload_data)

		return True
		

	def on_error(self, status):
		print 'error:', status


	on_event = on_status

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

myStream = Stream(auth, MyStreamListener())
myStream.filter(track=['nike','adidas','vans','movie','drink','burger king','chinese food','theatre',
                        'ktv','machine','gym','weekend','app','weichat','camel','marlboro','china','cs',
                         'travel','location','IBM','google','amazon','fish','hp','apple','iphone','pizza','money',
                        'train','subway','car','nyu','new york','election','dota','lol','game','party',
                        'icloud','google drive','twitter','instagram','snapchat','message','facebook','nba',
                       'microsoft','technology', 'weather','cloudy','rain','snow','food','baseball', 'football','tennis',
                      'sports','america','restaurant','hotel','song','taix','bike','devil may cry',
                     'nodejs','java','python','django','github','news','computer','health','medicine'])
