import twitter_app_src as tw
from datetime import date

start_date = tw.time_seven_days()
end_date = tw.time_now()

# Make filename
right_now = date.today()
week = right_now.strftime("%W")  # print week number
year = right_now.strftime("%Y")
tt_filename = f'./tt_csv_{year}/tt_week{week}.csv'

# Get tweets
tweet = tw.get_tweets(start=start_date, end=end_date)
tw_users = tw.make_twitter_users(tweets=tweet)

tw.make_twitter_csv(csv_file=tt_filename,
                    tweets=tweet,
                    users=tw_users)
