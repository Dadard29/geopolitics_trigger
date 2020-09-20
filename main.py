from env import *
import tweepy
from stream import MyStreamListener, log


def main():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    log("connected to api")

    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)

    leMondeId = "24744541"
    stream.filter(follow=[leMondeId])

    log("streaming...")
    stream.disconnect()


if __name__ == "__main__":
    main()
