# import tweepy
# import pandas as pd

# # Twitter API credentials
# consumer_key = 'FSa0Dws7tEkCC1imstR9ND9s3'
# consumer_secret = '2Q5WzPsORbiZwycWOAfzSjvWi6UIxw1eBHRq0BXhYlU3jhs2iG'
# access_token = '1676812625882279936-zmRQmxI4g73eASisHIQuoRGsUhqJBv'
# access_token_secret = 'hbVKHdxgUZqjqTYysqriKfyVVN5f4qjDwUHUfP9nzGHQg'

# #Pass in our twitter API authentication key
# auth = tweepy.OAuth1UserHandler(
#     consumer_key, consumer_secret,
#     access_token, access_token_secret
# )

# #Instantiate the tweepy API
# api = tweepy.API(auth, wait_on_rate_limit=True)

# # Define the query parameters
# query = 'good'
# tweet_count = 100  # Number of tweets to scrape

# # Scrape the tweets
# tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended').items(tweet_count)

# # Create a list to store the scraped data
# data = []
# for tweet in tweets:
#     data.append([tweet.user.screen_name, tweet.full_text])

# # Create a DataFrame using the scraped data
# df = pd.DataFrame(data, columns=['Username', 'Tweet'])

# # Save the DataFrame to a CSV file
# df.to_csv('twitter_data.csv', index=False)


# import tweepy

# # Set up your Twitter API credentials
# consumer_key = "E2Rpm9PDhfhv1dfGAPkwHpFRa"
# consumer_secret = 'rmUM4Kz9766RpUabNKUgmAGaC9Enlk5lR8ogwN6IsPCwC5nEqO'
# access_token = '1676812625882279936-0NZoDXdhgt7zJ1fyMTqgFmDzo92pO3'
# access_token_secret = 'kXDDShDfWSlgQePyCdGbrl6g0NKX8Tv1r7Et5D5QuVshw'

# # Authenticate with Twitter API
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# # Create API object
# api = tweepy.API(auth)

# # Define the username or Twitter user ID for the account you want to scrape
# username = "@zobiafyp28"


# query = 'good'
# # Set the number of tweets you want to scrape
# number_of_tweets = 100

# # Scrape the tweets
# tweets = api.user_timeline(screen_name=username, count=number_of_tweets, tweet_mode="extended")

# # Process and print the scraped tweets
# for tweet in tweets:
#     print(tweet.full_text)


# import requests
# from bs4 import BeautifulSoup

# url = 'https://twitter.com/search?q=hello'

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# tweets = soup.find_all('div', {'data-testid': 'tweet'})

# for tweet in tweets:
#     tweet_text = tweet.find('div', {'class': 'css-901oao'}).text.strip()
#     print(tweet_text)


# import GetOldTweets3 as got

# # Define the query parameters for scraping tweets
# tweet_criteria = got.manager.TweetCriteria().setQuerySearch('good').setMaxTweets(100)

# # Scrape tweets using GetOldTweets3
# tweets = got.manager.TweetManager.getTweets(tweet_criteria)

# # Process and print the scraped tweets and their comments
# for tweet in tweets:
#     print("Tweet:", tweet.text)
    
#     # Scrape comments of the tweet
#     tweet_id = tweet.id
#     comments = got.manager.TweetManager.getComments(tweet_id)
    
#     for comment in comments:
#         print("Comment:", comment.text)


# import twint

# # Configure the Twint search parameters
# c = twint.Config()
# c.Search = "hello"  # Replace with your desired search query
# c.Limit = 100  # Set the maximum number of tweets to retrieve

# # Run the Twint search
# twint.run.Search(c)

# # Process the scraped tweets
# for tweet in twint.output.tweets_list:
#     print(tweet.tweet)

# import scrapy
# from scrapy.selector import Selector


# class MySpider(scrapy.Spider):
#     name = "myspider"
#     allowed_domains = ["twitter.com"]
#     start_urls = ["http://www.twitter.com"]

#     def parse(self, response):
#         # Extract data using XPath selectors
#         data = response.xpath("//div[@class='myclass']/text()").extract()
#         yield {
#             'data': data
#         }
