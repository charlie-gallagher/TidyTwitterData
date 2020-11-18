import twitter_app_src as tw
import gmail_api
from datetime import date


today = date.today()
start_date = tw.time_24_hours()
end_date = tw.time_now()

tweet = tw.get_tweets(start=start_date, end=end_date)
tw_users = tw.make_twitter_users(tweets=tweet)

msg = tw.tweet_text(tweets=tweet, users=tw_users)
msg = f"Twitter update\nDate: {today}\n\n" + msg

gmail_api.send_twitter_email(tw_msg=msg, today=today)



