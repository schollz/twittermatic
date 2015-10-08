"""YATA

This is a true twitter bot that makes it easy to 
make friends, and bulk follow-back or unfollow people.

WITH GREAT POWER COMES GREAT RESPONSIBILITY.

Try not to abuse this script. Check the config.json file for 
parameters that change how aggressive this bot will try to 
make friends. 

Notes:

- When you reach 2,000 followers, you will not be able to add any more. 
  Currently this script doesn't ever check how many followers you have,
  so it will just keep trucking even though it won't be following people
  after 2,000. When you reach 2,000 just run twitterbot.py unfollow to 
  get rid of folks.

- There are random sleeps throughout the script to make it "look" 
  more like a real person is interacting with the site.
  
"""

import random
import json
import os
import re
import logging
from os import walk
from time import sleep, time
import multiprocessing

#import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import praw

import utils
import data.database as database
import data.database_commands as database_commands

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='twitterbot.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
selenium_logger = logging.getLogger(
    'selenium.webdriver.remote.remote_connection')
# Only display possible problems
selenium_logger.setLevel(logging.WARNING)

# Generic functions

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





class TwitterBot(object):
    """TwitterBot object
    
    Public Methods:
    
    signin()              -   Signs in the user
    screenshot()          -   Takes screen shot
    unfollow()            -   Unfollows in bulk
    followback()          -   Follow back in bulk
    collectTweets(handle) -   Collects tweets for the given handle
    liveSearch(term)      -   Loads all the tweets that match search term
    processFeed()         -   After using liveSearch(term) you can use this to process the tweets in feed
    makefriends()         -   Follow/Favorite/Reply/Retweet in bulk using search terms (does liveSearch + processFeed)
    tweet(text)           -   Tweets the given text
    generateTweet(subreddt) - Generates a tweet from something "hot" in that subreddit
    logout()              -   Signs out and closes down driver
    """

    def __init__(self, settingsFile, tor=False):
        """Initialize Twitter bot

        Inputs:     settingsFiles - name of settings file
                    tor (optional) - True/False for whether to use tor
        """

        database.init_db()

class TwitterBot(object):

    def __init__(self, settingsFile, tor=False):
        database.init_db()
        self.settings = json.load(open(settingsFile, 'r'))
        self.settings['file'] = settingsFile
        self.tor = tor
        self.logger = logging.getLogger(self.settings['file'])
        self.signedIn = False
        self.twittername = self.settings['twittername']
        self.logger.debug('Initialized')

    def signin(self):
        """Signs in user

        Loads the driver and signs in.
        After signing in it gets new data
        """
        self.profile = webdriver.FirefoxProfile()
        self.driver = webdriver.Firefox(self.profile)

        user = self.settings['username']
        psw = self.settings['password']

        if self.tor:
            self.logger.debug('Using TOR')
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.socks', '127.0.0.1')
            profile.set_preference('network.proxy.socks_port', 9050)

        # sign-in
        self.driver.get("http://www.twitter.com")
        sleep(1)

        # Log in is the button in the upper right in this case
        css = '.' + 'Button StreamsLogin js-login'.replace(' ', ',')
        login_buttons = self.driver.find_elements(By.CSS_SELECTOR, css)
        loginSuccess = False
        try:
            if len(login_buttons) > 0:
                self.logger.debug('Using login method 1')
                for button in login_buttons:
                    if "log" in button.text.lower():
                        button.click()
                        sleep(0.1)
                elems = self.driver.find_elements(
                    By.CSS_SELECTOR, '.text-input')
                elems[0].send_keys(user)
                sleep(0.1)
                elems[1].send_keys(psw + Keys.RETURN)
                loginSuccess = True
        except:
            pass
        if not loginSuccess:
            try:
                self.logger.debug('Using login method 2')
                eleme = self.driver.find_element_by_css_selector(
                    '.front-signin.js-front-signin')
                elem = eleme.find_element_by_css_selector(
                    '.text-input.email-input')
                elem.send_keys(user)
                elem = eleme.find_element_by_css_selector(
                    '.text-input.flex-table-input')
                elem.send_keys(psw + Keys.RETURN)
                loginSuccess = True
            except:
                pass
        if not loginSuccess:
            self.logger.error('No login method has worked!')
        self.logger.debug(self.driver.current_url)
        self.signedIn = loginSuccess
        self._getStats()

    def screenshot(self, filename=None):
        """Takes a screenshot."""
        self.logger.info("Taking a screenshot")
        if not filename:
            filename = str(time.time())
        if '.png' not in filename:
            filename += '.png'
        savefile = os.path.join('screenshots', filename)
        self.driver.save_screenshot(savefile)
        
    def unfollow(self):
        """Unfollow in bulk

        Goes to following page and unfollows 60% of followers,
        skipping the first 600.
        """
        if not self.signedIn:
            self.signin()

        self.driver.get(
            "http://www.twitter.com/" + self.settings['twittername'] + '/following')

        for i in range(60):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(.2)

        skip = 0
        blocks = self.driver.find_elements(
            By.CSS_SELECTOR, ".Grid-cell.u-size1of2.u-lg-size1of3.u-mb10")
        for block in blocks:
            text = str(block.text.encode('ascii', 'ignore'))
            skip += 1
            if ('FOLLOWS YOU' not in text or
                    random.randint(1, 100) <= 0.6) and skip > 600:
                css = '.' + \
                    'user-actions-follow-button js-follow-btn follow-button btn small small-follow-btn'.replace(
                        ' ', '.')
                button = block.find_elements(By.CSS_SELECTOR, css)[0]
                button.click()

        self.logger.debug(self.driver.current_url)
        self._getStats()

    def makefriends(self):
        """Follow/Favorite/Retweet/Reply in bulk
        
        Searches for specified search terms (in configuration)
        Goes through tweets and follows/favorites/retweets/replies based on probabilities
        """
        if not self.signedIn:
            self.signin()

        if self.settings['following'] > 1800:
            self.unfollow()

        # Generate search terms
        search_expressions = self.settings['search_expressions']
        avoid_words = self.settings['avoid_words']
        search_avoid_words = self.settings['search_avoid_words']

        search_terms = []
        for exp in search_expressions:
            search_terms.append('"' + exp + '" ' + '-' + ' -'.join(search_avoid_words) + ' since:' + (datetime.now() - timedelta(
                days=1)).strftime("%Y-%m-%d") + ' until:' + (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))

        for search_term in search_terms:
            self.logger.info(
                'Seeking out [' + search_term + '] for ' + self.settings['twittername'])
            self.liveSearch(search_term)
            self.tweetboxes = self._loadAllTweets(numTimes=1)
            self.processFeed()

    def _loadAllTweets(self, numTimes=1000):
        """Loads all the available tweets
        
        When searching or loading feed, you can use this function load 
        tweets by continuing scrolling to the bottom until no more tweets load
        (or numTimes reached)
        """
        lastNum = 0
        newNum = 1
        num = 0
        while lastNum != newNum and num < numTimes:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(.2)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(.2)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(.2)
            lastNum = newNum
            tweetboxes = self.driver.find_elements(By.CSS_SELECTOR,
                                                   ".js-stream-item.stream-item.stream-item.expanding-stream-item")
            num += 1
            newNum = len(tweetboxes)

        return tweetboxes

    def collectTweets(self, twitterhandle):
        """Collects all/latest tweets
        
        Input:  twitterhandle - Twitter handle of the user to grab tweets from
        
        Saves tweets to the database.
        """
        if not self.signedIn:
            self.signin()

        if '@' in twitterhandle:
            twitterhandle = twitterhandle.split('@')[1]

        #self.driver.get("http://www.twitter.com/" + twitterhandle)
        sleep(1)

        self.liveSearch('from:' + twitterhandle)

        boxInd = 0
        lastNumBoxes = 0
        self.tweetboxes = self._loadAllTweets(numTimes=1)
        numBoxes = len(self.tweetboxes)
        inserted = True
        while lastNumBoxes != numBoxes and inserted:
            while boxInd < len(self.tweetboxes) and inserted:
                tweetbox = self.tweetboxes[boxInd]
                tweet = self._getTweetStats(tweetbox)
                tweet['handle'] = twitterhandle
                inserted = database_commands.insertTweet(tweet) 
                boxInd += 1
            if inserted:
                self.tweetboxes = self._loadAllTweets(numTimes=5)
                lastNumBoxes = numBoxes
                numBoxes = len(self.tweetboxes)

        self.logger.info(
            'Inserted ' + str(boxInd - 1) + ' tweets for ' + twitterhandle)

    def _getTweetStats(self, tweetbox):
        """Gets Tweet information
        
        Input:      tweetbox - from a feed
        Returns:    dictionary containing tweet text, time, type, itemid, favorites, retweets
        """
        tweet = {}
        tweet['text'] = self._getTweetText(tweetbox)
        tweet['time'] = self._getTweetTime(tweetbox)
        tweet['type'] = tweetbox.get_attribute("data-item-type")
        tweet['itemid'] = tweetbox.get_attribute("data-item-id")
        words = tweetbox.text.split('\n')
        try:
            tweet['favorites'] = utils.convertCondensedNum(
                words[words.index('Retweet') + 1])
        except:
            tweet['favorites'] = -1
        try:
            tweet['retweets'] = utils.convertCondensedNum(
                words[words.index('Favorite') + 1])
        except:
            tweet['retweets'] = -1
        return tweet

    def liveSearch(self, search_term):
        """Gets Tweet information
        
        Input:      tweetbox - from a feed
        Returns:    dictionary containing tweet text, time, type, itemid, favorites, retweets
        """
        if not self.signedIn:
            self.signin()

        self.driver.get(
            "http://www.twitter.com/" + self.settings['twittername'])
        sleep(1)
        elem = self.driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys(search_term + Keys.RETURN)
        sleep(1)
        if not self.settings['topResults']:
            self.driver.find_element_by_css_selector(
                '.AdaptiveFiltersBar-target.AdaptiveFiltersBar-target--more.u-textUserColor.js-dropdown-toggle').click()
            sleep(1)
            self.driver.find_element_by_css_selector(
                "a[href*='f=tweets']").click()
            sleep(1)

        self.logger.debug(self.driver.current_url)
        if 'search' not in self.driver.current_url and search_term.split()[0] not in self.driver.current_url:
            self.logger.error('Problem with searching')
            
        self.driver.find_element_by_css_selector(
                '.AdaptiveSearchTitle-title').click()

    def processFeed(self):
        for tweetbox in self.tweetboxes:
            self.tweetbox = tweetbox
            tweetbox_text = tweetbox.text.split()
            twitter_handles = []
            all_twitter_handles = []
            dontEngage = False

            # check if you need to avoid this person
            if not dontEngage:
                for word in self.settings['avoid_words']:
                    if word in tweetbox.text.lower():
                        dontEngage = True
                        self.logger.info("need to avoid " + word)
                        break

            self.handle = self._getTweetHandle(tweetbox)
            if self.handle is not None:
                if database_commands.hasHandle(self.handle, self.twittername): 
                    dontEngage = True
                if not dontEngage:
                    problem = self._processTweet(tweetbox)
                else:
                    self.logger.info('Already interacted with ' + self.handle)

    def _processTweet(self, tweetbox):
        self.driver.execute_script(
                "window.scrollTo(0, %s);" % str(tweetbox.location['y'] + 100))

        database_commands.add(self.handle, self.twittername)
        if random.randint(1, 100) <= self.settings['followingProbability']:
            try:
                self._clickFollow(tweetbox)
            except:
                self.logger.error('Error following!')
        if random.randint(1, 100) <= self.settings['favoritingProbability']:
            try:
                self._clickFavorite(tweetbox)
            except:
                self.logger.error('Error favoriting!')
        if random.randint(1, 100) <= self.settings['retweetingProbability']:
            try:
                self._clickRetweet(tweetbox)
            except:
                self.logger.error('Error retweeting!')
        if random.randint(1, 100) <= self.settings['replyProbability']:
            try:
                self._clickReply(tweetbox)
            except:
                self.logger.error('Error replying!')
        return False

    def _getTweetText(self, tweetbox):
        tweet = tweetbox.find_element(By.TAG_NAME, "div")
        tweet = tweet.find_element(By.CSS_SELECTOR, "div.content")
        tweet_text = tweet.find_element(
            By.CSS_SELECTOR, "p.tweet-text").text#.decode("utf-8") #.encode('utf-8')
        tweet_text = str(tweet_text)
        tweet_text = tweet_text.replace('\n', '')
        return tweet_text

    def _getTweetTime(self, tweetbox):
        tweet = tweetbox.find_element(By.TAG_NAME, "div")
        tweet = tweet.find_element(By.CSS_SELECTOR, "div.content")
        tweet_time = tweet.find_element(
            By.CSS_SELECTOR, "div.stream-item-header")
        tweet_time = tweet_time.find_element(By.CSS_SELECTOR, "small.time")
        tweet_time = tweet_time.find_element(By.TAG_NAME, "a")
        tweet_time = tweet_time.find_element(
            By.CSS_SELECTOR, "span._timestamp")
        tweet_time = tweet_time.get_attribute("data-time")
        tweet_time = int(tweet_time)
        return tweet_time

    def _getTweetHandle(self, tweetbox):
        #for text in unidecode(tweetbox.text).split():
        for text in tweetbox.text.split():
            if '@' in text and len(text) > 4:
                return text
        return None

    def _clickTweetBox(self, tweetbox):
        self.logger.info('Clicking ' + tweetbox.text.split('\n')[0])
        clickSuccess = False
        try:
            li = tweetbox.find_element(By.CSS_SELECTOR, "div")
            li.click()
            clickSuccess = True
        except:
            pass
        if not clickSuccess:
            try:
                self.logger.warn('Clicking using method 2')
                li = tweetbox.find_element(
                    By.CSS_SELECTOR, ".tweet.original-tweet.js-stream-tweet.js-actionable-tweet.js-profile-popup-actionable.js-original-tweet.with-user-actions")
                li.click()
                clickSuccess = True
            except:
                pass
        if not clickSuccess:
            try:
                self.logger.warn('Clicking using method 3')
                li = tweetbox.find_element(
                    By.CSS_SELECTOR, ".tweet.original-tweet.js-stream-tweet.js-actionable-tweet.js-profile-popup-actionable.js-original-tweet.favorited.with-non-tweet-action-follow-button")
                li.click()
                clickSuccess = True
            except:
                pass
        if not clickSuccess:
            try:
                self.logger.warn('Clicking using method 4')
                li = tweetbox.find_element(
                    By.CSS_SELECTOR, ".tweet.original-tweet.js-stream-tweet.js-actionable-tweet.js-profile-popup-actionable.js-original-tweet.with-non-tweet-action-follow-button")
                li.click()
                clickSuccess = True
            except:
                pass

    def _clickFavorite(self, tweetbox):
        css = '.' + \
            'ProfileTweet-actionButton ProfileTweet-follow-button js-tooltip'.replace(
                ' ', ',')
        buttons = tweetbox.find_elements(By.CSS_SELECTOR, css)
        button_num = 0
        for button in buttons:
            if ("Favorite" in button.text):
                button.click()
                sleep(0.1)
                self.logger.debug('Favorited ' + self.handle)

    def _clickRetweet(self, tweetbox):
        css = '.' + \
            'ProfileTweet-actionButton ProfileTweet-follow-button js-tooltip'.replace(
                ' ', ',')
        buttons = tweetbox.find_elements(By.CSS_SELECTOR, css)
        button_num = 0
        for button in buttons:
            if ("Retweet" in button.text):
                button.click()
                sleep(0.5)
                css = 't1-form tweet-form RetweetDialog-tweetForm isWithoutComment condensed'
                css = '.' + css.replace(' ', '.')
                retweet_box = self.driver.find_element(By.CSS_SELECTOR, css)
                css = '.btn.primary-btn.retweet-action'
                sleep(0.5)
                retweet_box.find_element(By.CSS_SELECTOR, css).click()
                self.logger.debug('Retweeted ' + self.handle)
                database_commands.addRetweet(self.handle, self._getTweetText(tweetbox), self.twittername)
                sleep(0.5)
                try:
                    css = 't1-form tweet-form RetweetDialog-tweetForm isWithoutComment condensed'
                    css = 'Icon Icon--close Icon--medium dismissIcon Icon--close Icon--medium dismiss'
                    css = '.' + css.replace(' ', '.')
                    exit = self.driver.find_element(By.CSS_SELECTOR, css)
                    exit.click()
                    return True
                except:
                    return True

    def _clickReply(self, tweetbox):
        css = '.' + \
            'ProfileTweet-actionButton ProfileTweet-follow-button js-tooltip'.replace(
                ' ', ',')
        buttons = tweetbox.find_elements(By.CSS_SELECTOR, css)
        button_num = 0
        for button in buttons:
            if ("Reply" in button.text):
                button.click()

        sleep(0.5)
        textbox = tweetbox.find_element(
            By.CSS_SELECTOR, ".tweet-box.rich-editor.notie")
        thereply = random.choice(self.settings['replies'])
        textbox.send_keys(thereply)
        twitter_button = tweetbox.find_element(
            By.CSS_SELECTOR, ".btn.primary-btn.tweet-action.tweet-btn.js-tweet-btn")
        twitter_button.click()
        sleep(0.5)
        responses = self.driver.find_elements(By.CSS_SELECTOR, ".message-text")
        for response in responses:
            self.logger.debug('Response to reply: ' + response.text)
        self.logger.info('Replied to ' + self.handle)
        sleep(0.3)

    def _clickFollow(self, tweetbox):
        """Click the follow button
        
        First hover over user name
        Then float cursor over to the follow button
        Then press it
        """
        # First get into view
        self.driver.execute_script(
            "window.scrollTo(0, %s);" % str(tweetbox.location['y'] - 100))

        css = '.' + \
            'fullname js-action-profile-name show-popup-with-id'.replace(
                ' ', ',')
        profile_text = tweetbox.find_elements(By.CSS_SELECTOR, css)[0]
        Hover = ActionChains(self.driver).move_to_element(profile_text)
        Hover.perform()
        sleep(1)
        try:
            css = '.' + \
                'profile-card ProfileCard with-banner component profile-header hovercard gravity-south weight-left'.replace(
                    ' ', ',')
            container = self.driver.find_elements(By.CSS_SELECTOR, css)[0]
        except:
            pass

        try:
            css = '.' + \
                'profile-card ProfileCard with-banner component profile-header hovercard gravity-north weight-left'.replace(
                    ' ', ',')
            container = self.driver.find_elements(By.CSS_SELECTOR, css)[0]
        except:
            pass

        try:
            sleep(0.5)
            #if (' not-following' in unidecode(container.get_attribute("innerHTML"))):
            if (' not-following' in container.get_attribute("innerHTML")):
                sleep(0.5)
                css = '.' + \
                    'user-actions-follow-button js-follow-btn follow-button btn small small-follow-btn'.replace(
                        ' ', ',')
                follow_button = container.find_elements(
                    By.CSS_SELECTOR, css)[0]
                follow_button.click()
                sleep(0.5)

            Hover = ActionChains(self.driver).move_to_element_with_offset(
                profile_text, 10, 10)
            Hover.perform()
            self.logger.debug('Followed ' + self.handle)
        except:
            pass

    def followback(self):
        """Follow anyone that is following you"""
        
        if not self.signedIn:
            self.signin()

        self.driver.get(
            "http://www.twitter.com/" + self.settings['twittername'] + '/following')

        for i in range(3):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(.05)

        css = "user-actions btn-group not-muting can-dm not-following"
        css = '.' + css.replace(' ', '.')
        followers = self.driver.find_elements(By.CSS_SELECTOR, css)
        for follower in followers:
            if "Following" not in follower.text:
                css = '.' + \
                    'user-actions-follow-button js-follow-btn follow-button btn small small-follow-btn'.replace(
                        ' ', '.')
                buttons = follower.find_elements(By.CSS_SELECTOR, css)
                for button in buttons:
                    button.click()
                    sleep(.5)

    def _typeLikeHuman(self, element, text, enter=False):
        """Types slowly like a human would"""
        for letter in text:
            element.send_keys(letter)
            sleep(float(random.randint(1, 100)) / 200.0)
        if enter:
            element.send_keys(Keys.RETURN)

    def tweet(self, text):
        self.driver.get("http://www.twitter.com/")
        css = '.' + 'tweet-box rich-editor notie'.replace(' ', '.')
        twitterbox = self.driver.find_elements(By.CSS_SELECTOR, css)
        if len(twitterbox) == 0:
            css = '.' + \
                'tweet-box rich-editor notie is-showPlaceholder'.replace(
                    ' ', '.')
            twitterbox = self.driver.find_elements(By.CSS_SELECTOR, css)

        self._typeLikeHuman(twitterbox[0], text)

        css = '.' + \
            'btn primary-btn tweet-action tweet-btn js-tweet-btn'.replace(
                ' ', '.')
        tweetbtn = self.driver.find_elements(By.CSS_SELECTOR, css)
        tweetbtn[0].click()

    def generateTweet(self,subreddit=None):
        """Generates tweet based on something in a Reddit subreddit
        
        Input:  subreddit (optional) - if not used, the config settings will be used
        """
        if not self.signedIn:
            self.signin()
        expressions = ['cool', 'Awesome!', 'Check it out!',
                       'My favorite!', 'The BEST', 'So awesome', 'I love this']
        r = praw.Reddit(user_agent='twitter-' + self.settings['twittername'])
        if subreddit is None:
            subreddit = self.settings['subreddit']
        submissions = r.get_subreddit(
            subreddit).get_hot(limit=50)
        for submission in submissions:
            if submission.media is not None and submission.ups > 0:
                self.tweet(random.choice(expressions) + ' ' + submission.url)
                break

    def logout(self):
        """Logs out and closes driver"""
        
        self.driver.get("http://www.twitter.com/")
        css = 'btn js-tooltip settings dropdown-toggle js-dropdown-toggle'
        logout_button = self.driver.find_elements(
            By.CSS_SELECTOR, '.' + css.replace(' ', '.'))
        logout_button[0].click()
        sleep(0.1)
        css = 'dropdown-link'
        dropdown_menu = self.driver.find_elements(
            By.CSS_SELECTOR, '.' + css.replace(' ', '.'))

        for menu in dropdown_menu:
            if 'Log out' in menu.text:
                menu.click()
                break

        if 'logged_out' in self.driver.current_url:
            self.logger.debug(
                'Logged out from ' + self.settings['twittername'])
        else:
            self.logger.error('Something went wrong with logging out')

        self.driver.close()
        self.signedIn = False

    def _getStats(self):
        """Gets stats from main page"""
        
        self.driver.get("http://www.twitter.com/")
        css = 'ProfileCardStats-statValue'
        following = self.driver.find_elements(
            By.CSS_SELECTOR, '.' + css.replace(' ', '.'))
        if 'K' in following[0].text:
            self.settings['tweets'] = float(
                following[0].text.replace('K', '')) * 1000
        else:
            self.settings['tweets'] = int(following[0].text)
        self.settings['following'] = int(following[1].text.replace(',', ''))
        self.settings['followers'] = int(following[2].text.replace(',', ''))
        self.logger.debug('Tweets: %s, Following: %s, Followers %s' % (
            following[0].text, following[1].text, following[2].text))
        with open(self.settings['file'], 'w') as f:
            f.write(json.dumps(self.settings, indent=4))


def getConfigFiles():
    f = []
    for (dirpath, dirnames, filenames) in walk('./data'):
        for filename in filenames:
            if '.json' in filename:
                f.append('./data/' + filename)
    return f


'''
# Load bots
bots = []
for f in getConfigFiles():
    print f
    bots.append(TwitterBot(f))
bots[0].collectTweets('lessig')


python
from lib import *
bot = TwitterBot('stefans.json')
bot.collectTweets('scotus')


'''



bot = TwitterBot('default2.json')
bot.makefriends()


