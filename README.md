# YATA (Yet Another Twitter Automator)

This set of Python classes helps to perform all sorts of Twitter activities, *without the use of API keys!* Instead, this utility is completely based of [Selenium for Python](https://github.com/SeleniumHQ/selenium). As such, any program using these tools is not restricted to any of the Twitter API limits - [retrieving a max of 3,200 statuses, aggressive following](https://dev.twitter.com/overview/general/things-every-developer-should-know) and the only thing you need is a Twitter Login.

What can YATA do?  You can [download a users entire Twitter feed](#collect-latest-tweets-from-somebody), [search a keyword and follow/retweet/reply/favorite those tweets](#do-a-live-search-for-cats-and-retweet-at-those-handles), [tweet stuff](#tweet-something), among some things. A full list of available functions are [listed below](#features). Now includes bundled support for [PhantomJS](http://phantomjs.org/)!

## Installation

```bash
pip install -r requirements.txt
```
Copy the config file into the ```data``` folder and edit it with your login details:

```bash
cp default.json ./data/default.json
```

## Usage

### ```makefriends()```

The function ```makefriends()``` is a special function that does a lot of automation based only on your configuration file. The ```default.json``` config file looks like:

```javascript
{
    "username": "YOUR USERNAME",
    "twittername": "YOUR TWITTER HANDLE",
    "password": "YOUR PASSWORD",
    "topResults": false,
    "retweetingProbability": 50,
    "replyProbability": 50,
    "favoritingProbability": 50,
    "followingProbability": 50,
    "search_expressions": [
        "#cats",
    ],
    "search_avoid_words": [
        "dog"
    ],
    "avoid_words": [
        "dog"
    ],
    "replies": [
        "I love cats!",
        "Cool!",
        "Awesome",
        ":)"
    ]
}
```

The first three parameters are most important - they are your Twitter sign-in details. The rest of the data is if you care to use the ```makefriends()```. For instance if you use:

```
from lib import *
bot = TwitterBot('default.json') # Load bot
bot.makefriends()
```

Then the bot will do the following:

1. Search for ```search_expressions``` minus the ```search_avoid_words```,  so it will search "#cats -dogs".
2. Load the entire feed
3. Go through tweets, one-by-one, skipping tweets that have the ```avoid_words```.
4. Go through each tweet and Follow/Favoite/Retweet/Reply based on the probabilities in the settings.
5. If the bot replies, it will randomly choose one of the ```replies```.

Another neat feature of ```makefriends()``` - if your bot signs in and it sees it has more than 1,800 followers, then it will automatically use ```unfollow()``` to unfollow some of them.


### Collect latest tweets from somebody

The following code will collect someone's tweets. The first time it runs it will collect **all** of that user's tweets. *All of them*. It takes about an hours per 10,000 tweets. On subsequent runs it will capture the neweset tweets, and then stop when it discoveres it already has the rest.

```python
from lib import *

bot = TwitterBot('default.json',headless=False)
bot.collectTweets('scotus') 
```

This will save all the tweets in a database ```data/tweets.db``` in a table called ```tweets``` with all the Twitter user information in a relational table ```handlers```.

**New feature** - if you'd like to use Phantom, simply set ```headless``` to ```True``` and it will automatically use the correct Phantom driver!.

### Do a live search for cats and retweet at those handles

This will go through and search for ```#cats``` and retweet, reply, and favorite the tweets depending on your set probabilities in ```default.json```.

```python
from lib import *

bot = TwitterBot('default.json') # Load bot
bot.liveSearch('#cats')
bot.loadEntireFeed()
bot.processFeed()
```

Any person that is interacted with is saved to the database  ```data/tweets.db``` in a table called ```cache```. Any retweet is also saved in a table ```tweets``` with ```type``` ```"rt"```.

### Tweet something

```python
from lib import *

bot = TwitterBot('default.json') # Load bot
bot.generateTweet()
```

## Features

Here is a list of the current public functions accessible from the ```TwitterBot``` class:

```bash
    signin()              -   Signs in the user
    screenshot()          -   Takes screen shot
    unfollow()            -   Unfollows in bulk
    followback()          -   Follow back in bulk
    collectTweets(handle) -   Collects tweets for the given handle
    liveSearch(term)      -   Loads all the tweets that match search term
    loadEntireFeed()      -   After doing a search, this can be used to load the entire feed
    processFeed()         -   After using liveSearch(term) you can use this to process the tweets in feed
    makefriends()         -   Follow/Favorite/Reply/Retweet in bulk using search terms 
                                (does liveSearch + loadEntireFeed + processFeed)
    tweet(text)           -   Tweets the given text
    generateTweet()       -   Generates a tweet from the corpus
    logout()              -   Signs out and closes down driver
```

## Known Issues

- If you retweet, but you are blocked by that user, the program will stop (it will not be able to exit the message that you are blocked). 

	Unfortunately, this happens too infrequently to be able to precisely evaluate and generate a work-around.

- Firefox will tend to cache a lot.

    To get around this, I suggest setting Firefox to "private" mode only. That way your passwords will also not be saved so you won't run into issues with automatic password filling in (which will throw the bot off).

- Elements dissapear before I can profile them!

    Use [Firefox Firebug](http://getfirebug.com/) for profiling things.

## To-do

- ~Simple generation of the settings file~
- ~Multiple accounts per settings file~
- ~Ability to iterate through all the current users~
- ~Add in memory of persons previously replied to/favorited~
- ~Add in the collector~
- Set the hasHandle to only retrive ones in the last week
- Add in callbacks for error handling
- Add in timer functions to exit

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

Note, that to profile the elements in the DOM, its very useful to use [Firefox Firebug](http://getfirebug.com/).

## History

- 10/12/2015: Added PhantomJS support

## Credits

TODO: Write credits

## License

The MIT License (MIT)

Copyright (c) 2015 Zack

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
