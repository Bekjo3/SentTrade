import praw

def setup_reddit(client_id, client_secret, user_agent):
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)
    return reddit

def scrape_reddit(reddit, subreddit, keyword):
    posts = []
    subreddit = reddit.subreddit(subreddit)
    for submission in subreddit.search(keyword, limit=10):
        posts.append(submission.title + ' ' + submission.selftext)
    return posts
