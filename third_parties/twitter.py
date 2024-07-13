import os
from dotenv import load_dotenv
import tweepy
import requests

load_dotenv()


# twitter_client = tweepy.Client(
#     bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
#     consumer_key=os.environ["TWITTER_API_KEY"],
#     consumer_secret=os.environ["TWITTER_API_KEY_SECRET"],
#     access_token=os.environ["TWITTER_ACCESS_TOKEN"],
#     access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
# )
# twitter needs us to pay around some 100$ for getting access to their API, so using the gist file instructor has provided


def scrape_user_tweets(username, num_tweets=5, mock: bool = False):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    tweet_list = []

    if mock:
        EDEN_TWITTER_GIST = "https://gist.githubusercontent.com/emarco177/827323bb599553d0f0e662da07b9ff68/raw/57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/eden-marco-twitter.json"
        tweets = requests.get(EDEN_TWITTER_GIST, timeout=5).json()

    else:
        user_id = twitter_client.get_user(username=username).data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
        )
        tweets = tweets.data

    for tweet in tweets:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":

    tweets = scrape_user_tweets(username="EdenEmarco177", mock=True) # Udemy instructor's twitter username
    print(tweets) # with mock=True, got response: [{'text': '🚨 Demo Alert: risks when deploying insecure LLM agents 🤖\n(Spoiler: total environment compromise!)🚨\n\nIn a recent demo, I showcased what happens when deploying an LLM Agent to the cloud without taking basic security measures.\nThe outcome was alarming☠️\nan exploitable… https://t.co/OKoxiOUFGQ https://t.co/DPi8aVcPls', 'url': 'https://twitter.com/EdenEmarco177/status/1767277531537744100'}, {'text': 'Contextual Answers from the @AI21Labs team is a fantastic model when you want the LLM to always stay within the provided context.\nThe main benefits for using this kind of model are:\n\n1.  Significant reduction in hallucinations, enhancing accuracy and reliability.\n\n2.  Improved… https://t.co/rqTuHdvOMU https://t.co/6OUIHorMrf', 'url': 'https://twitter.com/EdenEmarco177/status/1766014021033972000'}]
