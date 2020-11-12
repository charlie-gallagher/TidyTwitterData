import twitter_app_src as tw

def main():
    print("=============================")
    print(" Welcome to the Tweet Getter")
    print("=============================")
    while True:
        action = input("\nCommand (e.g. get-tweets): ")
        if action == "get-tweets":
            print("\n")
            start_date = tw.time_seven_days()
            end_date = tw.time_now()

            tweet = tw.get_tweets(start=start_date, end=end_date)

            # Check for tweet response errors
            try:
                print("\nERROR:" + tweet[0]["title"])
                print(tweet[0]["errors"][0]["message"])
                return
            except KeyError:  # will throw KeyError if no error present
                pass

            twitter_users = tw.make_twitter_users(tweets=tweet)

            print("\nTweets retrieved.")
            make_csv = input("Make a CSV? (y/n): ")
            if make_csv == "y":
                filename = input("Filename: ")
                tw.make_twitter_csv(csv_file=filename,
                                    tweets=tweet,
                                    users=twitter_users)
            elif make_csv == "n":
                tw.print_tweets(tweets=tweet, users=twitter_users)
            else:
                print("Input not recognized.")
        elif action == "exit":
            return


if __name__ == "__main__":
    main()