import logging
import datetime
from data.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create Database Driver/Engine
engine = create_engine('sqlite:///data/tweets.db', echo=False)

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()


import os
import csv

def create_tweet(**kwargs):
    """ Creates a user and assigns it to a group """
    logger = logging.getLogger('DatabaseCommands.create_tweet')
    logger.info("Saving tweet to database")
    query = session.query(Tweet).filter(Tweet.data_id == kwargs['data_id'])
    if len(query.all()) == 0:
        dt = datetime.datetime.utcfromtimestamp(kwargs['tweet_time'])
        try:
            tweet = Tweet(
                            twitter_handle=kwargs['twitter_handle'], 
                            tweet_time=dt, 
                            tweet_text=kwargs['tweet_text'], 
                            data_type=kwargs['data_type'], 
                            data_id=kwargs['data_id'],
                            status=kwargs['status']
                        )
            session.add(tweet)
            session.commit()
            logger.info("Saved tweet " + str(kwargs['data_id']) + " to database")
            logger.debug("twitter_handle = " + str(kwargs['twitter_handle']))
            logger.debug("tweet_time = " + str(kwargs['tweet_time']))
            logger.debug("tweet_text = " + str(kwargs['tweet_text']))
            logger.debug("data_type = " + str(kwargs['data_type']))
            logger.debug("data_id = " + str(kwargs['data_id']))
            logger.debug("status = " + str(kwargs['status']))
            return True
        except Exception as e:
            print(e)
            session.rollback()
            logger.error("Error occurred saving tweet " + kwargs['data_id'] + " to database")
            logging.error(e)
            return False
    else:
        logger.warning("Tweet " + kwargs['data_id'] + " already exists")

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






'''


    def add(self, handle):
        if not self.hasHandle(handle):
            cmd = """INSERT INTO cache (twittername,repliedhandle) VALUES ('%s','%s')""" % (
                self.twittername, handle)
            self.c.execute(cmd)
            self.conn.commit()

    def addRetweet(self, handle, tweet):
        try:
            cmd = """INSERT INTO retweets (twittername,repliedhandle,tweet) VALUES ('%s','%s','%s')""" % (
                self.twittername, handle, tweet.replace("'", "''"))
            self.c.execute(cmd)
            self.conn.commit()
        except:
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