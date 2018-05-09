from __future__ import print_function
import tweepy
import json
import MySQLdb 
from dateutil import parser

COORDINATES = [-94.8115,38.857,-94.3982,39.2895]
LOCATION = 'Kansas City'

CONSUMER_KEY = "KEY"
CONSUMER_SECRET = "SECRET"
ACCESS_TOKEN = "TOKEN"
ACCESS_TOKEN_SECRET = "TOKEN_SECRET"

HOST = "mysql.cis.ksu.edu"
USER = "myusername"
PASSWD = "mypassword"
DATABASE = "mydatabase"

# This function takes the 'created_at', 'text', 'screen_name' and 'tweet_id' and stores it
# into a MySQL database
def store_data(created_at, text, screen_name, tweet_id, lang):
    db=MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")
    cursor = db.cursor()
    insert_query = "INSERT INTO twitter (tweet_id, screen_name, created_at, text, lang, location) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (tweet_id, screen_name, created_at, "", lang, LOCATION))
    db.commit()
    cursor.close()
    db.close()
    return

class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
           # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            #grab the wanted data from the Tweet
            text = datajson['text']
            screen_name = datajson['user']['screen_name']
            tweet_id = datajson['id']
            created_at = parser.parse(datajson['created_at']) 
            lang = datajson['lang']

            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
            
            #insert the data into the MySQL database
            store_data(created_at, text, screen_name, tweet_id, lang)
        
        except Exception as e:
           print("Exception Caught")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + LOCATION)
streamer.filter(locations=COORDINATES)
