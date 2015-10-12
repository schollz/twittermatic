import datetime
from data.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime


class Handler(Base):
    __tablename__ = 'handlers'
    id = Column(Integer, primary_key=True)
    handle = Column(String(50), unique=True)
    firstname = Column(String(150), unique=False)
    lastname = Column(String(150), unique=False)
    location = Column(String(150), unique=False)
    website = Column(String(150), unique=False)
    bio = Column(String(300), unique=False)
    tweets = relationship("Tweet", backref="tweets")
    #tweets = Column(Integer, ForeignKey("tweets.id"))
    Timestamp =Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, handle, firstname=None, lastname=None, location=None, website=None, bio=None):
        self.handle = handle
        self.firstname = firstname
        self.lastname = lastname
        self.location = location
        self.website = website
        self.bio = bio

    def __repr__(self):
        return '<Handler %r>' % (self.handle)


class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    handle = Column(String(50), unique=False)
    tweet_time = Column(DateTime, unique=False)
    text = Column(String(150), unique=False)
    type = Column(String(50), unique=False)
    itemid = Column(String(120), unique=False)
    retweets = Column(Integer, unique=False)
    favorites = Column(Integer, unique=False)
    status = Column(Integer, unique=False)
    handler_id = Column(Integer, ForeignKey("handlers.id"))
    Timestamp =Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, twitter_handle=None, tweet_time=None, tweet_text=None, data_type=None, data_id=None, retweets=None, favorites=None, status=None):
        self.handle = twitter_handle
        self.tweet_time = tweet_time
        self.text = tweet_text
        self.type = data_type
        self.itemid = str(data_id)
        self.retweets = int(retweets)
        self.favorites = int(favorites)
        self.status = status
        #Timestamp = Column(DateTime, unique=False)

    def __repr__(self):
        return '<Tweet %r>' % (self.tweet_text)


class Cache(Base):
    __tablename__ = 'cache'
    id = Column(Integer, primary_key=True)
    twittername = Column(String(50), unique=False)
    repliedhandle = Column(String(50), unique=False)
    Timestamp =Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, twittername=None, repliedhandle=None):
        self.twittername = twittername
        self.repliedhandle = repliedhandle

    def __repr__(self):
        return '<Cache %r>' % (self.repliedhandle)

'''
class Retweet(Base):
    __tablename__ = 'retweets'
    id = Column(Integer, primary_key=True)
    twittername = Column(String(50), unique=False)
    repliedhandle = Column(String(50), unique=False)
    text = Column(String(150), unique=False)
    Timestamp =Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, twittername=None, repliedhandle=None, text=None):
        self.twittername = twittername
        self.repliedhandle = repliedhandle
        self.text = text

    def __repr__(self):
        return '<Cache %r>' % (self.repliedhandle)

'''