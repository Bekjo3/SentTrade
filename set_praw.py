import praw

def setup_reddit(client_id, client_secret, user_agent, username, password):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        username=username,
        password=password
    )
    return reddit

def scrape_reddit(reddit, subreddit_name, keyword, from_date, to_date, limit=50):
    subreddit = reddit.subreddit(subreddit_name)
    query = f"{keyword} timestamp:{from_date}..{to_date}"
    posts = subreddit.search(query, sort='new', limit=limit, time_filter='all')
    return [post.title + " " + post.selftext for post in posts]
