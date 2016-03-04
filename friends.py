from lib import *
from random import random
from time import sleep

# Load bots
bots = []
for f in getConfigFiles():
    bots.append(TwitterBot(f))


while True:
    for i in range(len(bots)):
        try:
            if random() < 0.02:
                bots[i].generateTweet()
        except:
            pass
        try:
            bots[i].makefriends()
        except:
            pass
        try:
            bots[i].logout()
        except:
            pass
    sleep(60)
