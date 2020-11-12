# Twitter
Let's clearly lay out the objective.

With Python or CMD or PowerShell or even C, I want to make an app that generates (or appends to) a JSON file with tweet performance. Actually, I could produce a CSV over time, and retrospectively for all my tweets.

This is the first step: my tweets and their performance. The second step is to analyze all Tidy Tuesday tweets and see how my tweets compare.

# Developer Twitter
I'm going to store my keys in a batch file that automatically adds them as environment variables in CMD. This is just to exercise my CMD variable setting syntax... I don't know what the equivalent in PowerShell is, except to declare a variable and dot-source it.

This post on [measuring tweet performance](https://developer.twitter.com/en/docs/tutorials/measure-tweet-performance) is my guide at the moment. Another good resource is the [Tweet Lookup Reference Guide](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets).

# Where will I develop this?
Python will be the easiest language to build it with. Alternatively, I could write it as a cmdlet for PowerShell or even a basic batch file for CMD. The last option is to do it directly in R. This has the perk of being in the place of analysis, but R isn't as flexible or fast as Python is. To Python, then!

Program options:

- Tweepy
- twitter

These are both used to interact with the API, and both handle OAuth, but Tweepy is a convenient wrapper so that's what I'm going to use. That way, I don't have to deal with JSON files.

# The Twitter API
There are two APIs right now, API v2 and API v1.1. Because Tweepy probably uses API 1.1, that's what I'm going to take notes on here. Understanding this one will probably help me understand V2 later, so no harm done.

## Tweet JSON
The Twitter API returns jSON files as tweets. A JSON file is made up of attributes (keys in Python) and values (values in Python). Both Tweets and Users are held as JSON objects, and there are various 'entity' objects for Tweet contents like hastags, mentions, media, and links.

The main object for Tweet data is the **Tweet Object**, which is parent to several child objects. This always includes a User object. Retweet objects and Quote Tweet objects may contain several Tweet objects, each with its own User object.

#### Retweets
Retweets contain a Tweet object for the original tweet and the retweet. The 'original' tweet is provided in a "retweeted_status" object. The root-level object encapsulates teh Retweet itself. Less information is available for retweets.

#### Quote Tweets
These also include a new Tweet message, which may be as rich as the original. The quoted Tweet is provided in the "quoted_status" object.

## Data Dictionary
The basic structure of a tweet is this:

- Tweet
  - User
  - Entities
  - Extended entities
  - Places

**Tweet** Also referred to as a ‘Status’ object, has many ‘root-level’ attributes, parent of other objects.

A basic example with _some_ of the common attributes and child objects.
```json
{
 "created_at": "Wed Oct 10 20:19:24 +0000 2018",
 "id": 1050118621198921728,
 "id_str": "1050118621198921728",
 "text": "To make room for more expression, we will now count all emojis as equal—including those with gender‍‍‍ ‍‍and skin t… https://t.co/MkGjXf9aXm",
 "user": {},
 "entities": {}
}
```

Other useful attributes for me:

- retweet_count
- favorite_count
- retweeted_status
- quoted_status
- is_quote_status

Note that Tweets were not always able to be 280 characters; older tweets were 140, and the API used to reflect this (and still does for backwards compatibility). Use `full_text` for the full text, rather than `text` which will truncate tweets longer than 140 characters. The boolean `truncated` will tell you whether the Tweet `text` is truncated.

**User** Twitter Account level metadata. Will include any available account-level enrichments, such as Profile geo.

Example:
```json
{ "user": {
    "id": 6253282,
    "id_str": "6253282",
    "name": "Twitter API",
    "screen_name": "TwitterAPI",
    "location": "San Francisco, CA",
    "url": "https://developer.twitter.com",
    "description": "The Real Twitter API. Tweets about API changes, service issues and our Developer Platform. Don't get an answer? It's on my website.",
    "verified": true,
    "followers_count": 6129794,
    "friends_count": 12,
    "listed_count": 12899,
    "favourites_count": 31,
    "statuses_count": 3658,
    "created_at": "Wed May 23 06:01:13 +0000 2007",
    "utc_offset": null,
    "time_zone": null,
    "geo_enabled": false,
    "lang": "en",
    "contributors_enabled": false,
    "is_translator": false,
    "profile_background_color": "null",
    "profile_background_image_url": "null",
    "profile_background_image_url_https": "null",
    "profile_background_tile": null,
    "profile_link_color": "null",
    "profile_sidebar_border_color": "null",
    "profile_sidebar_fill_color": "null",
    "profile_text_color": "null",
    "profile_use_background_image": null,
    "profile_image_url": "null",
    "profile_image_url_https": "https://pbs.twimg.com/profile_images/942858479592554497/BbazLO9L_normal.jpg",
    "profile_banner_url": "https://pbs.twimg.com/profile_banners/6253282/1497491515",
    "default_profile": false,
    "default_profile_image": false,
    "following": null,
    "follow_request_sent": null,
    "notifications": null
  }
}
```

Note that `id` and `id_str` are for the user here, not for the Tweet. Any reference to Tweet.id will return the Tweet's ID, while Tweet.user.id will return the User's ID, which never changes. The `screen_name` is the user's handle.

**Entities** Containes object arrays of hashtags, mentions, symbols, URLs, and media.

Every tweet JSON will include an 'entities' section with `hashtags`, `urls`, `user_metions`, and `symbols`, at least. For working with photos, videos, and GIFs, use an Extended Entities Object instead.


Example:

```json
"entities": {
    "hashtags": [
        {
          "indices": [
            32,
            38
          ],
          "text": "nodejs"
        }
    ],
    "urls": [
        {
            "indices": [
              32,
              52
          ],
        "url": "http://t.co/IOwBrTZR",
        "display_url": "youtube.com/watch?v=oHg5SJ…",
        "expanded_url": "http://www.youtube.com/watch?v=oHg5SJYRHA0"
        }
    ],
    "user_mentions": [
        {
          "name": "Twitter API",
          "indices": [
            4,
            15
          ],
          "screen_name": "twitterapi",
          "id": 6253282,
          "id_str": "6253282"
        }
    ],
    "symbols": [
    ]
  }
```

**Extended Entities** Contains up to four native photos, or one video or animated GIF.

This is preferred for dealing with photos because it includes all photos, rather than only the first photo (which is what the entities object does).

Here is a very long example of an extended entities object with four photos.

```json
{
"extended_entities": {
    "media": [
      {
        "id": 861627472244162561,
        "id_str": "861627472244162561",
        "indices": [
          68,
          91
        ],
        "media_url": "http://pbs.twimg.com/media/C_UdnvPUwAE3Dnn.jpg",
        "media_url_https": "https://pbs.twimg.com/media/C_UdnvPUwAE3Dnn.jpg",
        "url": "https://t.co/9r69akA484",
        "display_url": "pic.twitter.com/9r69akA484",
        "expanded_url": "https://twitter.com/FloodSocial/status/861627479294746624/photo/1",
        "type": "photo",
        "sizes": {
          "medium": {
            "w": 1200,
            "h": 900,
            "resize": "fit"
          },
          "small": {
            "w": 680,
            "h": 510,
            "resize": "fit"
          },
          "thumb": {
            "w": 150,
            "h": 150,
            "resize": "crop"
          },
          "large": {
            "w": 2048,
            "h": 1536,
            "resize": "fit"
          }
        }
      },
      {
        "id": 861627472244203520,
        "id_str": "861627472244203520",
        "indices": [
          68,
          91
        ],
        "media_url": "http://pbs.twimg.com/media/C_UdnvPVYAAZbEs.jpg",
        "media_url_https": "https://pbs.twimg.com/media/C_UdnvPVYAAZbEs.jpg",
        "url": "https://t.co/9r69akA484",
        "display_url": "pic.twitter.com/9r69akA484",
        "expanded_url": "https://twitter.com/FloodSocial/status/861627479294746624/photo/1",
        "type": "photo",
        "sizes": {
          "small": {
            "w": 680,
            "h": 680,
            "resize": "fit"
          },
          "thumb": {
            "w": 150,
            "h": 150,
            "resize": "crop"
          },
          "medium": {
            "w": 1200,
            "h": 1200,
            "resize": "fit"
          },
          "large": {
            "w": 2048,
            "h": 2048,
            "resize": "fit"
          }
        }
      },
      {
        "id": 861627474144149504,
        "id_str": "861627474144149504",
        "indices": [
          68,
          91
        ],
        "media_url": "http://pbs.twimg.com/media/C_Udn2UUQAADZIS.jpg",
        "media_url_https": "https://pbs.twimg.com/media/C_Udn2UUQAADZIS.jpg",
        "url": "https://t.co/9r69akA484",
        "display_url": "pic.twitter.com/9r69akA484",
        "expanded_url": "https://twitter.com/FloodSocial/status/861627479294746624/photo/1",
        "type": "photo",
        "sizes": {
          "medium": {
            "w": 1200,
            "h": 900,
            "resize": "fit"
          },
          "small": {
            "w": 680,
            "h": 510,
            "resize": "fit"
          },
          "thumb": {
            "w": 150,
            "h": 150,
            "resize": "crop"
          },
          "large": {
            "w": 2048,
            "h": 1536,
            "resize": "fit"
          }
        }
      },
      {
        "id": 861627474760708096,
        "id_str": "861627474760708096",
        "indices": [
          68,
          91
        ],
        "media_url": "http://pbs.twimg.com/media/C_Udn4nUMAAgcIa.jpg",
        "media_url_https": "https://pbs.twimg.com/media/C_Udn4nUMAAgcIa.jpg",
        "url": "https://t.co/9r69akA484",
        "display_url": "pic.twitter.com/9r69akA484",
        "expanded_url": "https://twitter.com/FloodSocial/status/861627479294746624/photo/1",
        "type": "photo",
        "sizes": {
          "small": {
            "w": 680,
            "h": 680,
            "resize": "fit"
          },
          "thumb": {
            "w": 150,
            "h": 150,
            "resize": "crop"
          },
          "medium": {
            "w": 1200,
            "h": 1200,
            "resize": "fit"
          },
          "large": {
            "w": 2048,
            "h": 2048,
            "resize": "fit"
          }
        }
      }
    ]
  }
}
```


**Places** Parent to 'coordinates' object.

This isn't applicable to my project.

# Querying
My standard, free searches will be limited to the last seven days and will be organized by relevance. They will not be complete. But a lot can be done, anyway.

The base url is `https://api.twitter.com/1.1/search/tweets.json`, and to this you usually add `?q=<request>&result_type=<result_type>`.

URLs use [Percent encoding](https://en.wikipedia.org/wiki/Percent-encoding), so here are some important codes:

- `#` %23
- `@` %40
- `:` %3A
- ` ` (space) %20
- `_` %5F
- `"` %22

The whole query goes in a `q` field. For example:

- `q=from%3ACmdr_Hadfield%20%23nasa&result_type=popular` is decoded as "find popular tweets from Cmdr_Hadfield with #nasa."
- `q=%23haiku+%23poetry` will search "haiku poetry."

Note: 'space' may be represented as either + or %20.

There are three references for making searches that will help.

1. [GET search tweets reference](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets)
2. [Twitter search standard operators](https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/overview/standard-operators)
3. [Percent-encoding on Wikipedia](https://en.wikipedia.org/wiki/Percent-encoding)

Some fields from the first link:

- q: UTF-8 percent-encoded search for the "search bar".
- result_type: Can be 'recent', 'popular', or 'mixed'.
- count: Results per page, defaults to 15, max 100.
- since_id: Returns results with ID greater than the specified ID
  - Note: Tweet IDs increase over time. I'm not sure how to find a specific time, like last Tuesday.


# Results
So far, the results aren't that impressive. One of the big problems right now is that most recent tweets are retweets. I didn't anticipate that... Of course, I can filter the results, but I don't think I can simply not return retweets, can I? According to the documentation, you can filter out retweets with `-filter:retweets`. This encodes to "-filter%3Aretweets". It didn't work. Why didn't it work? Not sure, I'm also having trouble with 'popular'.

I filtered retweets with '-RT', which works because every retweet is prefixed with 'RT'. Doesn't present an obvious way to filter out replies, though.

I used the following call with good results:

```py
import tweepy
import keys

# OAuth 2 verification
auth = tweepy.OAuthHandler(_api_key, _api_secret_key)
api = tweepy.API(auth)

tt = api.search(q="%23TidyTuesday%20-RT", result_type="mixed",
                count=25,
                tweet_mode="extended")
for i in tt:
    print(i.full_text)
    print('-------------')
```

Because this will end up on Github at some point, I should save a file that contains the keys and add it to the .gitignore.



# Twitter's new API
The new API is much better than the old one. I've started using it without a wrapper, because the wrappers weren't that impressive, and none support the new API. Instead, I'm using plain `requests` to get the job done, and it's going really great. The `requests` module builds URLs from common Python objects, so I like the simplicity of that.

There are improved data and fields, and it's very simple to use once you get the hang of it. There's one downside: you have to connect different dataset.

# Update
So, some things have changed. I combined most of my utility files into `twitter_app_src.py`, so see that folder for the bulk of the programming. I scheduled `twitter_scheduled_program.py` to run every week on Monday at 11:59 PM. That will get all Tweets from midnight the previous Tuesday. It automatically names the files, so now I just have to wait for an entire year before having a nice usable dataset... With that, I'm pretty much done with the general purpose project for now.

The next project I want to do is detailed personal data so that I can anlyze my tweets' performances throughout the week. Also, I need to set up the Git for this repository and push it online. That means writing a README and cleaning up the files so they are presentable-ish. 
