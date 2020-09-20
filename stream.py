import tweepy

from datetime import datetime
import requests

from env import *


def log(msg):
    print(str(datetime.now()), msg)


def send_to_geoplitics(article_link, hashtags, brief):
    body = {
        "article_link": article_link,
        "hashtags": hashtags,
        "tweet_text": brief
    }

    headers = {
        "X-Access-Token": SUB_TOKEN
    }
    resp = requests.post(f"{GEOP_HOST}/relationships/pending", json=body, headers=headers)
    return resp.status_code == 200, resp.json()["Message"]


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__(api)
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        try:
            log(f"{tweet.user.name}\t tweeted:  {tweet.text}")
            if tweet.user.name == "Le Monde":
                if tweet.truncated:
                    url_obj = tweet.extended_tweet['entities']['urls'][0]
                    display_link = url_obj['display_url']

                    # check if is international
                    if display_link.startswith("lemonde/international"): # FIXME
                        article_link = url_obj['expanded_url']
                        hashtags = [h['text'] for h in tweet.extended_tweet['entities']['hashtags']]
                        tweet_text = tweet.extended_tweet['full_text']

                        # send to geop
                        status, msg = send_to_geoplitics(article_link, hashtags, tweet_text)
                        if status:
                            log("sent")
                        else:
                            log(f"failed to send: {msg}")

        except Exception as e:
            log("failed to process tweet")
            log(str(e))

    def on_error(self, status):
        log("Error detected")
        log(status)

