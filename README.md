# Twitter
Every week, I contribute to Tidy Tuesday. To satisfy my curiosity about (1) how my own tweets are doing, (2) how other tweets are doing, (3) how many tweets there were this week, I wrote a few Python programs that get Twitter data and convert it to a CSV.

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

In addition, there are several email files, the most important of which are `twitter_email.py` and `gmail_api.py`. There is a scatter-brained note file called `twitter_email_notes.md` as well, which contains some useful information about email and encryption protocols (viz. SMTP, TLS, and MIME).

# Examples
## Command line interface
Running `py twitter_app.py` in a shell

```
> py twitter_app.py
=============================
 Welcome to the Tweet Getter
=============================

Command (e.g. get-tweets): get-tweets


Getting first tweet page...
Getting other pages...
No more tokens.

Tweets retrieved.
Make a CSV? (y/n): n
Handle                   Likes    Retweets   Quotes  Replies
------                   -----    --------   ------  -------
Priyesh7401                  2           1        0        1
lauren_swensen               1           0        1        0
colinlecoque                 1           0        0        0
redcat84                     6           0        0        0
karmanizcaked                1           0        0        0
violet_ventur                3           0        0        2
LLung08                      9           1        0        1
GDataScience1               24           6        1        2
JesseRoe55                  31           6        2        1
zachbogart                   1           0        0        0
princesxxxpeach             15           0        1        3
DanNdanuko                   9           0        0        1
NoriCeleste                  5           1        0        1
CharlieGallaghr              4           3        0        0
paulapivat                   2           1        0        0
paulapivat                   5           1        0        1
rladiesbuchares              1           1        0        0
ThotsKenyan                 30           4        0        2
CameCry                      4           0        0        0
HelenJYan                    2           0        0        0
MyQueenHell                 11           1        0        0
lukorir                      5           1        0        0
Juanma_MN                    6           2        0        1
jakekaupp                   39           3        0        3
thomas_mock                179          63       12        4
cnicault                    32           7        0        1
louisenynke                 25           3        1        2
cashleyi                     3           1        0        0
jinglebelllzzz               7           1        0        1
Ken27204002                  2           1        0        0
Ken27204002                  2           1        0        0
vinaypratap                  9           1        1        0
Artest38145967               4           1        0        4
BayskPMA                     7           1        0        3
blake_reavis                 2           1        0        0
sydney_oberg                 3           1        0        0
KathyCh01362181              5           2        0        1
rogg_and_roll                4           1        0        0
FurusethThomas               0           0        0        0
arnabp123                   13           5        1        0
thomas_mock                  3           2        0        0
balt_ti                     11           5        0        0
geokaramanis                10           1        0        0
MYMRockMama                 10           4        0        1
GoldenB16117397              7           3        0        0
lanahuynhh                   3           0        0        1
KathyCh01362181              6           2        0        1
Nathan63592879               6           1        0        0
ehp2468                      8           3        0        0
ramsicafrente                3           2        0        0
datasciencejenn             10           3        0        1
toeb18                      32           4        2        0
jorgelsm                     6           1        0        1
johnmutiso_                 18           2        0        1
CedScherer                  44           5        2        1
CedScherer                 122          11        2        6
KT_The_Lady                 12           2        1        0
larsivanjanzen               7           1        0        1
AbiolaPAyodele               9           1        0        1
sianbladon                  23           7        0        4
CharlieGallaghr             14           5        0        2
kustav_sen                  40           7        0        0
smakeneni15                  6           3        0        1
denis_mongin                 8           5        0        0

Command (e.g. get-tweets): exit
```

The only accepted command at thet moment is `get-tweets`. This automatically gets the tweets from the last 168 hours (7 days). The user is prompted to say whether they would like to create a CSV file or not. If not, the program automatically displays the most recent tweets with basic information.

If, rather, you select 'y' when prompted to make a CSV:

```
=============================
 Welcome to the Tweet Getter
=============================

Command (e.g. get-tweets): get-tweets


Getting first tweet page...
Getting other pages...
No more tokens.

Tweets retrieved.
Make a CSV? (y/n): y
Filename: trash_csv.csv
CSV written to trash_csv.csv
Command (e.g. get-tweets): exit
```

The file is by default saved to the local folder, and all filenames are relative to the local working directory.

## Scheduled program
The file `twitter_scheduled_program.py` automatically generates a CSV from the last seven days of tweets, names it `tt_week##.csv` where `##` is the TidyTuesday week or close to it. The file is saved in a folder called  `tt_csv_yyyy` where `yyyy` is the current year.

## Sending email
The `twitter_email.py` program sends an email of summary statistics from the last 24 hours to, at the moment, my email. You can edit this file to make it send from or to any email you want, but the 'from' email has to be a Gmail account. If the email was successful, you will get an email ID returned to the terminal.

## Using `twitter_app_src.py` to build your programs
The `twitter_app_src.py` file contains several useful and fairly general functions for dealing with the Twitter data.

- `get_tweets(start, end)`
  - Takes a start datetime (ISO 8601) and end datetime. Returns a list of twitter page results (one page per list item). Each page is a Pythonized JSON file returned by the Twitter API. The request may be modified here.
- `make_twitter_users(tweets)`
  - Creates a dictionary of users, which is essential for attaching usernames to user IDs and tweets. `tweets` is the result of `get_tweets()`. The format is `{"id": ["id", "name", "username"], ...}`. To get a user's handle: `users["id"][2]`, where `id` is the user's ID returned in the API response.
- `make_twitter_csv(csv_file, tweets, users)`
  - Convert a twitter API response to a simplified CSV file.
- `print_tweets(tweets, users)`
  - Print a summary of the tweets from the response contained in `tweets` and `users`.
- `tweet_text(tweets, users)`
  - Similar to `print_tweets`, but output is a single string object containing the data.
- `time_now()`, `time_24_hours()`, `time_seven_days()`
  - Convenience functions which output a string datetime in ISO 8601 format.


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

# Setting up Email
I recently added an email feature so that Tweet data can easily be sent to any email(s) you want. The files associated with this are `gmail_api.py` and `twitter_email.py`. The former interacts with the GMail API and the latter creates a formatted email with the Twitter data. At the moment, the email is a single text string, but perhaps a better implementation is to use a file system. A text file is easier to generate probably than a text string, and easier to check. Then simply read in the text file as a long string and off you go. But while the emails are relatively simple, this just adds unnecessary complexity.

Google's GMail API uses OAuth2.0 to authorize users, and once you are a developer user, this authorization will be started automatically from the app. First, you need credentials, which you can get from the GMail Python [quickstart page](https://developers.google.com/gmail/api/quickstart/python). Follow the instructions bu don't run their `startup.py` file; it works but it's written for Python 2.7, not 3.8. In `google_api.py`, I give an updated version of this file. The first time you run it (and any time you delete `token.pickle`) it will redirect you to GMail to allow permission to the app. The refresh token expires every hour or fiftenn minutes or something, but it is automatiacally refreshed by the function.

In sum, to get email to work, you must use GMail, and you have to have GMail API credentials in your working directory as per the quickstart page.
