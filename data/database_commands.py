
import logging
import datetime
import traceback
from data.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create Database Driver/Engine
engine = create_engine('sqlite:///data/tweets.db', echo=False)
logger = logging.getLogger('db_cmds')
# Create a Session
Session = sessionmaker(bind=engine)
session = Session()


def get_tweet_by_id(tweet_id):
    """ Get Tweet by ID 

        @param tweet_id     {String} id of tweet
    """
    query = session.query(Tweet).filter(Tweet.itemid == tweet_id)
    results = query.all()
    if len(results) > 0:
        return results
    else:
        return None

def get_tweet_by_handle(handle):
    """ Get Tweet by handle 

        @param handle     {String} handle of user
    """
    query = session.query(Tweet).filter(Tweet.handle == handle)
    results = query.all()
    return results

def getHandler(handle):
    """ Twitter Handle 

        @param handle     {String} handle of user
    """
    query = session.query(Handler).filter(Handler.handle == handle)
    results = query.all()
    return results

def hasHandle(repliedhandle, twittername):
    """ Check if handle exists 

        @param repliedhandle    {String} handle of user
        @param twittername      {String} handle of current user
    """
    query = session.query(Cache).filter(Cache.repliedhandle == repliedhandle).filter(Cache.twittername == twittername)
    results = query.all()
    return len(results) > 0

def add(repliedhandle, twittername):
    """ Add to cache 

        @param repliedhandle    {String} handle of user
        @param twittername      {String} handle of current user
    """
    if not hasHandle(repliedhandle, twittername):
        try:
            cache = Cache(twittername,repliedhandle)
            session.add(cache)
            session.commit()
        except:
            print("ERROR WRITING CACHE")
            session.rollback()

def addRetweet(repliedhandle, tweet, twittername):
    """ Adds retweet 

        @param repliedhandle    {String} handle of user
        @param twittername      {String} handle of current user
        @param tweet            {String} text of tweet
    """
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

def insertTweet(details, insertDuplicates=True):
    """ Adds tweet to database 

        @param details          {Dict} contains tweet details
        @param insertDuplicates   {Boolean} optional, if true it
                                    will insert even if already exists
    """
    try:
        if not insertDuplicates:
            if get_tweet_by_id(details['itemid']) != None:
                return False
        tweet = Tweet(
            twitter_handle=details['handle'], 
            tweet_time=datetime.datetime.utcfromtimestamp(details['time']), 
            tweet_text=details['text'], 
            data_type=details['type'], 
            data_id=details['itemid'], 
            retweets=details['retweets'], 
            favorites=details['favorites'], 
            status=1
        )
        session.add(tweet)
        session.commit()
        addTweetToHandler(tweet,details['handle'])
        return True
    except Exception as e:
        traceback.print_exc()
        traceback.print_stack()
        print("ERROR OCCURED WHEN INSERTING TWEET")
        print(e)
        session.rollback()
        return False

def addTweetToHandler(tweet,twitterhandler):
    """ Adds tweet to handler in database
        if user isn't in database one will be created.

        @param tweet            {Tweet} Tweet model object
        @param twitterhandler   {String} handler of twitter user
    """
    handles = getHandler(twitterhandler)
    if len(handles) < 1:
        user = {}
        user['handle'] = twitterhandler
        user['firstname'] = None
        user['lastname'] = None
        user['location'] = None
        user['website'] = None
        user['bio'] = None
        insertTwitterHandler(user)
        handler = getHandler(twitterhandler)[0]
    else:
        handler = handles[0]
    try:
        handler.tweets.append(tweet)
        session.commit()
    except:
        session.rollback()

def insertTwitterHandler(user):
    """ Adds twitter handler to database

        @param user     {Dict} Contains user details
    """
    try:
        handle = Handler(
            handle = user['handle'],
            firstname = user['firstname'],
            lastname = user['lastname'],
            location = user['location'],
            website = user['website'],
            bio = user['bio']
        )
        session.add(handle)
        session.commit()
        return True
    except Exception as e:
        traceback.print_exc()
        traceback.print_stack()
        print("ERROR OCCURED WHEN INSERTING USER")
        print(e)
        session.rollback()
        return False

