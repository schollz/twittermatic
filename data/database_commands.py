
import logging
import datetime
import traceback
from data.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create Database Driver/Engine
engine = create_engine('sqlite:///data/tweets.db', echo=False)

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()


def get_tweet_by_id(tweet_id):
    """ Get Tweet by ID """
    query = session.query(Tweet).filter(Tweet.data_id == data_id)
    results = query.all()
    if len(results) == 1:
        return query.one()
    elif len(results) == 0:
        return None
    else:
        raise ValueError("Duplicate tweets")

def get_tweet_by_handle(handle):
    """ Get Tweet by handle """
    query = session.query(Tweet).filter(Tweet.twitter_handle == handle)
    results = query.all()
    return results




def hasHandle(repliedhandle, twittername):
    query = session.query(Cache).filter(Cache.repliedhandle == repliedhandle).filter(Cache.twittername == twittername)
    results = query.all()
    return len(results) > 0

def add(repliedhandle, twittername):
    if not hasHandle(repliedhandle, twittername):
        try:
            cache = Cache(twittername,repliedhandle)
            session.add(cache)
            session.commit()
        except:
            print("ERROR WRITING CACHE")
            session.rollback()

def addRetweet(repliedhandle, tweet, twittername):
    print ("-"*30)
    print(tweet)
    print ("-"*30)
    try:
        retweet = Retweet(twittername,repliedhandle,tweet)
        session.add(retweet)
        session.commit()
    except:
        print("ERROR OCCURED WHEN INSERTING RETWEET")
        session.rollback()


def insertTweet(tweet, skipDuplicates=True):
    try:
        #for item in tweet:
        #    print(item,type(tweet[item]),tweet[item])
        tweet = Tweet(
            twitter_handle=tweet['handle'], 
            tweet_time=datetime.datetime.utcfromtimestamp(tweet['time']), 
            tweet_text=tweet['text'], 
            data_type=tweet['type'], 
            data_id=tweet['itemid'], 
            retweets=tweet['retweets'], 
            favorites=tweet['favorites'], 
            status=1
        )
        session.add(tweet)
        session.commit()
        return True
    except Exception as e:
        traceback.print_exc()
        traceback.print_stack()
        print("ERROR OCCURED WHEN INSERTING TWEET")
        print(e)
        session.rollback()
        return False


'''
class Database(object):

    def __init__(self, twittername):
        self.logger = logging.getLogger(twittername)
        self.twittername = twittername
        self.conn = sqlite3.connect("./data/data.db")
        self.c = self.conn.cursor()
        try:
            self.c.execute("""CREATE TABLE cache(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                twittername TEXT, 
                repliedhandle TEXT, 
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
        except:
            print("Table already exists")
        try:
            self.c.execute("""CREATE TABLE retweets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                twittername TEXT, 
                repliedhandle TEXT, 
                tweet TEXT, 
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
        except:
            print("Table already exists")
        try:
            self.c.execute("""CREATE TABLE tweets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                handle TEXT, 
                text TEXT, 
                tweet_time INTEGER, 
                retweets INTEGER, 
                favorites INTEGER, 
                type TEXT, 
                itemid INTEGER, 
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
        except:
            print("Table already exists")


def hasHandle(repliedhandle, twittername):
    query = session.query(Tweet).filter(Tweet.repliedhandle == repliedhandle).filter(Tweet.twittername == twittername)
    results = query.all()
    return len(results) > 0

def add(repliedhandle, twittername):
    if not hasHandle(handle):
        try:
            cache = Cache(twittername,repliedhandle)
            session.add(cache)
            session.commit()
        except:
            print("ERROR WRITING CACHE")
            session.rollback()

def addRetweet(repliedhandle, tweet, twittername):
    try:
        retweet = Retweet(twittername,repliedhandle,tweet)
        session.add(retweet)
        session.commit()
    except:
        print("ERROR OCCURED WHEN INSERTING RETWEET")
        session.rollback()


def insertTweet(tweet, skipDuplicates=True):
    try:
        #for item in tweet:
        #    print(item,type(tweet[item]),tweet[item])
        retweet = Tweet(
            twitter_handle=tweet['handle'], 
            tweet_time=datetime.datetime.utcfromtimestamp(tweet['time']), 
            tweet_text=tweet['text'], 
            data_type=tweet['type'], 
            data_id=tweet['itemid'], 
            retweets=tweet['retweets'], 
            favorites=tweet['favorites'], 
            status=None
        )
        session.add(retweet)
        session.commit()
        return True
    except Exception as e:
        traceback.print_exc()
        traceback.print_stack()
        print("ERROR OCCURED WHEN INSERTING TWEET")
        print(e)
        session.rollback()
        return False
=======
            print("ERROR OCCURED WHEN INSERTING TWEET")

    def hasHandle(self, handle):
        cmd = """SELECT repliedhandle FROM cache WHERE repliedhandle LIKE '%s' and twittername like '%s' LIMIT 1""" % (
            handle, self.twittername)
        self.c.execute(cmd)
        foundOne = False
        for row in self.c.fetchall():
            foundOne = True
            break
        return foundOne

    def hasTweet(self, tweet):
        cmd = """SELECT * FROM tweets WHERE handle LIKE '%s' and text like '%s' and tweet_time = %s LIMIT 1""" % (
            tweet['handle'], tweet['text'], str(tweet['time']))
        self.c.execute(cmd)
        foundOne = False
        for row in self.c.fetchall():
            foundOne = True
            break
        return foundOne

    def insertTweet(self, tweet, skipDuplicates=True):
        tweet['text'] = tweet['text'].replace("'", "''")
        if (self.hasTweet(tweet) and skipDuplicates):
            self.logger.info('Have rest of tweets for ' + tweet['handle'])
            return False
        else:
            cmd = """INSERT INTO tweets (handle,text,tweet_time,retweets,favorites,type,itemid) VALUES ('%s','%s',%s,%s,%s,'%s',%s)""" % (
                tweet['handle'], tweet['text'], str(tweet['time']), str(tweet['retweets']), str(tweet['favorites']), str(tweet['type']), str(tweet['itemid']))
            self.logger.info(cmd)
            self.c.execute(cmd)
            self.conn.commit()
            return True
'''
