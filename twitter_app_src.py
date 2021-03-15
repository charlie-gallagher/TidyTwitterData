import requests
import keys
import csv
import datetime


def get_tweets(start, end):
    header = {"authorization": f"Bearer {keys.bearer_token}"}
    uri = "https://api.twitter.com/2/tweets/search/recent"
    parameters = {
        "query": "#TidyTuesday -is:retweet has:media -titty -#findom",
        "max_results": 100,
        "tweet.fields": "public_metrics,created_at",
        "expansions": "author_id,attachments.media_keys",
        "start_time": start,
        "end_time": end
    }

    print("Getting first tweet page...")
    tweet_request = requests.get(url=uri, params=parameters, headers=header)
    tweet = [tweet_request.json()]

    print("Getting other pages...")
    try:
        i = 0  # i = index of last tweet set (set containing key for next one)
        while tweet[i]["meta"]["next_token"]:
            parameters["next_token"] = tweet[i]["meta"]["next_token"]
            tweet_request = requests.get(url=uri, params=parameters,
                                         headers=header)
            tweet.append(tweet_request.json())
            i += 1
            print(f"Got {i} more tweet JSONs")

    except KeyError:
        print("No more tokens.")

    return tweet


def make_twitter_users(tweets):
    """
    Generate a twitter user dictionary.

    :param tweets: List of tweet JSON files from Twitter API
    :return: Dictionary of users and attributes
    """
    twitter_users = {}
    for page in tweets:
        for tw in page["includes"]["users"]:
            twitter_users[tw["id"]] = [tw["id"], tw["name"], tw["username"]]
    return twitter_users


def make_twitter_csv(csv_file, tweets, users):
    """
    Convert a twitter JSON and a user dictionary to a CSV file

    :param csv_file: Filename of CSV
    :param tweets: List of JSON responses from Twitter API
    :param users: User dictionary made by make_twitter_user
    :return: None
    """
    with open(file=csv_file, mode="w", encoding="utf-8") as twcsv:
        tw_writer = csv.writer(twcsv)
        tw_writer.writerow(['tweet_id', 'created_at', 'text',
                            'likes', 'retweets', 'quotes', 'replies',
                            'userid', 'user_name', 'username'])
        for page in tweets:
            for tw in page["data"]:
                tw_text = tw["text"]
                tw_id = tw["id"]
                tw_created_at = tw["created_at"]
                likes = tw["public_metrics"]["like_count"]
                retweets = tw["public_metrics"]["retweet_count"]
                quotes = tw["public_metrics"]["quote_count"]
                replies = tw["public_metrics"]["reply_count"]
                userid = tw["author_id"]
                username = users[userid][2]
                user_name = users[userid][1]
                tw_writer.writerow([tw_id, tw_created_at, tw_text,
                                    likes, retweets, quotes, replies,
                                    userid, user_name, username])
    print(f"CSV written to {csv_file}")


def print_tweets(tweets, users):
    """
    Print a summary of the tweet data
    :param tweets: JSON-like Python object
    :param users: Dictionary of users and attributes
    :return: None
    """

    print("Handle                   Likes    Retweets   Quotes  Replies")
    print("------                   -----    --------   ------  -------")
    for page in tweets:
        for tw in page["data"]:
            likes = tw["public_metrics"]["like_count"]
            retweets = tw["public_metrics"]["retweet_count"]
            quotes = tw["public_metrics"]["quote_count"]
            replies = tw["public_metrics"]["reply_count"]
            userid = tw["author_id"]
            username = users[userid][2]

            print(f"{username:25}{likes:5}{retweets:12}{quotes:9}{replies:9}")

def tweet_text(tweets, users):
    """
    Return a summary of the tweet data as a list of strings
    :param tweets: JSON-like Python object
    :param users: Dictionary of users and attributes
    :return: Formatted tweet text as a single string
    """

    tweet_txt = ["Handle                   Likes    Retweets   Quotes  "
                 "Replies", "------                   -----    --------   "
                            "------  -------"]
    for page in tweets:
        for tw in page["data"]:
            likes = tw["public_metrics"]["like_count"]
            retweets = tw["public_metrics"]["retweet_count"]
            quotes = tw["public_metrics"]["quote_count"]
            replies = tw["public_metrics"]["reply_count"]
            userid = tw["author_id"]
            username = users[userid][2]

            tweet_txt.append(
                f"{username:25}{likes:5}{retweets:12}{quotes:9}{replies:9}"
            )
        output = '\n'.join(tweet_txt)
        return output

# Generating valid dates
def time_now():
    """ Return string current time

    NOTE: The hour offset needs to be updated with daylight savings

    """
    t = datetime.datetime.now() - datetime.timedelta(minutes=10)
    return t.strftime("%Y-%m-%dT%H:%M:%S-04:00")

def time_24_hours():
    """ Return string of nearly one day ago """
    t = datetime.datetime.now() - datetime.timedelta(hours=23,
                                                     minutes=59,
                                                     seconds=0)
    return t.strftime("%Y-%m-%dT%H:%M:%S-04:00")

def time_seven_days():
    """ Return string of nearly seven days ago """
    t = datetime.datetime.now() - datetime.timedelta(days=6,
                                                     hours=23,
                                                     minutes=59,
                                                     seconds=0)
    return t.strftime("%Y-%m-%dT%H:%M:%S-04:00")
