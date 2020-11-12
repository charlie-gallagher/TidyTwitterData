# Twitter
Every week, I contribute to Tidy Tuesday. I wonder how I'm doing compared to the other Tidy Tuesday tweets, and whether a bad week for me is becaues of my visualization or because no one is paying attention to Tidy Tuesday this week. To satisfy that desire, I wrote a few Python programs that get Twitter data and convert it to a CSV.

Important note: Twitter places several restrictions on their public API. First, you need a developer account to make requests from the API. Second, the search feature only returns results from the last seven days; hence, historical data on Tidy Tuesday is unavailable.

The Twitter API itself is beyond the scope of this document. I used the new Twitter API (2.0) rather than the old one. There are fewer restrictions and the results are cleaner. The functions are up-to-date as of November 12, 2020.

# Setup
Before using these scripts and functions, you need to set up a [Twitter developer account](https://developer.twitter.com/en/apply-for-access). Once you have your keys, you will need to make a file `keys.py` in the same location as this respository. The `keys.py` file should be formatted in this manner:

```py
api_key = "your_api_key"
api_secret_key = "your_secret_key"
bearer_token = "your_bearer_token"
```


# Introduction
There are three principle files:

- `twitter_app_src.py`: Functions for getting Tweets from the Twitter API. These can be printed or converted to a CSV.
- `twitter_app.py`: A very basic command line interface. This is really just a convient wrapper of the functions in the `src` file; the user actually has very few paths through the `main` function.
- `twitter_scheduled_program.py`: An application of the Twitter functions that will get the Tweets from the last seven days (from exactly now to exactly seven days ago) and export the data to a properly titled CSV.

# Twitter API Interface
There are several Twitter API modules available (e.g. `python-twitter` or `tweepy`) but these do not allow for easy formatting of the GET query, and they do not use the new API. Also, I'm not working with OAuth1.0 user verification, so a simple HTTP interface will work fine. I am using the `requests` module, which allows for simple formatting of the GET request url, which is _very_ convenient for modifying the URL to accommodate a changing page key. (Page keys are important for Twitter search result [pagination](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/paginate).)

The authorization is peformed using an HTML GET request header formatted thus: `"authorization"="Bearer <bearer_token>"`. As long as you include a properly formatted `keys.py` file, this is taken care of for you.

The request I submit is as follows:

```py
import requests
import keys

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

tweet_request = requests.get(url=uri, params=parameters, headers=header)
```

Where `start` and `end` are parameters passed to the function. These must by formatted as ISO 8601 times, and they are strictly interpreted. If the specified time is out of Twitter's range (from exactly seven days ago to exactly now), an error response is returned instead of a JSON. So, it's more convenient to generate these with the `datetime` module than to type them in yourself.

The API is very flexible (read: complicated), so rather than describe why I chose the parameters I did, I'm going to direct you to these documentation pages:

- [General API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Search Requests Documentation](https://developer.twitter.com/en/docs/twitter-api/tweets/search/introduction)
- [Formatting Twitter Searches](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-rule)
