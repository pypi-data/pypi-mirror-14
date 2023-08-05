global reddit_client_id
global reddit_client_secret
global reddit_client_refresh
global reddit_redirect_uri
global twitter_consumer_key
global twitter_consumer_key_secret
global twitter_access_token
global twitter_access_token_secret

# https://apps.twitter.com/app/new
twitter_consumer_key = 'px2E2wOhxNrs4tsr8JqojB2yp'
twitter_consumer_key_secret = 'zyVTNh7x2BUCDChlsZ6OStSqhFBBI8nEBWDGKv2HXcIfMbmLJg'
twitter_access_token = '2563910439-Spw0P4vTwqfxAhvegQGXcDxPuGIFpv9cxHeLn8N'
twitter_access_token_secret = 'IDYvhgDMyka6oEWVJgZbBTVyWIk1njDYyjPUnVlRLlgZe'

# https://www.reddit.com/prefs/apps/
reddit_client_id = 'eoAG6V7plEDeAA'
reddit_client_secret = 'lXYyUycvBhfDzu6r6kkr3LlOoHA'
reddit_client_refresh = '32851213-sqXSqxYRTXADXJaR2sg7VTRNtIo'
reddit_redirect_uri = 'http://127.0.0.1"'


# How to get the reddit refresh token
#
#
# https://praw.readthedocs.org/en/stable/pages/oauth.html#step-4-exchanging-the-code-for-an-access-token-and-a-refresh-token
#
# 1) Get an access token:
# url = r.get_authorize_url('uniqueKey', 'submit', True)
# import webbrowser
# webbrowser.open(url)
# Copy the access token from the addressbar
#
# https://praw.readthedocs.org/en/stable/pages/oauth.html#step-6-refreshing-the-access-token
#
# 2) Get the refresh token:
# access_information = r.get_access_information('CODE YOU GOT ABOVE')
# print(access_information['refresh_token'])
