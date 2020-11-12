# Twitter
Every week, I contribute to Tidy Tuesday. I wonder how I'm doing compared to the other Tidy Tuesday tweets, and whether a bad week for me is becaues of my visualization or because no one is paying attention to Tidy Tuesday this week. To satisfy that desire, I wrote a few Python programs that get Twitter data and convert it to a CSV.

Important note: Twitter places several restrictions on their public API. First, you need a developer account to make requests from the API. Second, the search feature only returns results from the last seven days; hence, historical data on Tidy Tuesday is unavailable.

The Twitter API itself is beyond the scope of this document. I used the new Twitter API (2.0) rather than the old one. There are fewer restrictions and the results are cleaner.

## Scheduled Tweet Getter
I scheduled `twitter_scheduled_program.py` to run every week on Monday at 11:59 PM. This will get all tweets containing \#TidyTuesday, barring those that are retweets, quote tweets, or replies. I have also restricted the search results to those tweets with some media (either a GIF or one or more pictures). I have done my best to filter the results containing tits.
