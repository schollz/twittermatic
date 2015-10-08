# YATA (Yet Another Twitter Automator)

This bot seeks to help users automate Twitter activities (friending, searching, unfollowing) *without the use of API keys!* Instead, this bot is completely based of [Selenium for Python](https://github.com/SeleniumHQ/selenium).


# Installation

```bash
pip install -r requirements.txt
```
Copy the config file into the ```data``` folder and edit it with your login details:

```bash
cp default.json ./data/default.json
```

## Usage

### Collect tweets from somebody

The following code will collect someones tweets. It will run until it has found that it already collected that tweet, so on the first time it will take awhile especially if that perseon has a ton of tweets.

```python
from lib import *

bot = TwitterBot('default.json') # Load bot
bot.collectTweets('scotus') 
```

### Do a live search for #cats and retweet at those handles

This will go through and search for ```#cats``` and retweet, reply, and favorite the tweets depending on your set probabilities in ```default.json```.

```python
from lib import *

bot = TwitterBot('default.json') # Load bot
bot.liveSearch('#cats')
bot.tweetboxes = self._loadAllTweets()
bot.processFeed()
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
    processFeed()         -   After using liveSearch(term) you can use this to process the tweets in feed
    makefriends()         -   Follow/Favorite/Reply/Retweet in bulk using search terms (does liveSearch + processFeed)
    tweet(text)           -   Tweets the given text
    generateTweet(subreddt) - Generates a tweet from something "hot" in that subreddit
    logout()              -   Signs out and closes down driver
```

## Known Issues

- If you retweet, but you are blocked by that user, the program will stop (it will not be able to exit the message that you are blocked). 

	Unfortunately, this happens too infrequently to be able to precisely evaluate and generate a work-around.

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

## History

TODO: Write history

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
