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
        retweet = Tweet(
            twitter_handle=tweet['handle'], 
            tweet_time=datetime.datetime.utcfromtimestamp(str(tweet['time'])), 
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
    except:
        print("ERROR OCCURED WHEN INSERTING TWEET")
        session.rollback()
        return False

