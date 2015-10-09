import csv
import json
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask.ext.triangle import Triangle
import data.database_commands as database_commands

app = Flask(__name__)
Triangle(app)


@app.route("/")
def index():
    handles = json.load(open('config.json','r'))['handles']
    results = ''
    for handle in handles:
        results += handle
        results += '<br>'
    return results


@app.route("/tweets")
def tweets():
    handle = request.args.get('handle')
    tweets = database_commands.get_tweet_by_handle(handle)
    data = []
    for tweet in tweets:
        arr = {
            "twitter_handle": str(tweet.twitter_handle),
            "tweet_time": str(tweet.tweet_time),
            "data_type": str(tweet.data_type),
            "data_id": str(tweet.data_id),
            "status": str(tweet.status),
            "tweet_text": str(tweet.tweet_text)
        }
        data.append(arr)
    return render_template('index.html',tweets=data,title=handle)

# @app.route("/tweets")
# def root():
#     handle = request.args.get('handle')
#     tweets = database_commands.get_tweet_by_handle(handle)
#     data = 'handle,timestamp,data_type,data_id,status,tweet_text<br>'
#     for tweet in tweets:
#         data += str(tweet.twitter_handle) + ","
#         data += str(tweet.tweet_time) + ","
#         data += str(tweet.data_type) + ","
#         data += str(tweet.data_id) + ","
#         data += str(tweet.status) + ","
#         data += str(tweet.tweet_text)
#         data += '<br>'
#     return data

@app.route("/export")
def export():
    handle = request.args.get('handle')
    tweets = database_commands.get_tweet_by_handle(handle)
    data = 'handle,timestamp,data_type,data_id,status,tweet_text\n'
    for tweet in tweets:
        data += str(tweet.twitter_handle)
        data += str(tweet.tweet_time)
        data += str(tweet.data_type)
        data += str(tweet.data_id)
        data += str(tweet.status)
        data += str(tweet.tweet_text)
        data += '\n'
    return Response(data, mimetype='text/csv')


if __name__ == '__main__':
    app.run(
        host= '0.0.0.0',
        debug=True, 
        port=8080
    )
