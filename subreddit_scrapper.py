import os
import praw
import time
from dotenv import load_dotenv
from typing import List

load_dotenv()
    
def get_scraped_submissions(tracked_subreddits, keywords):
    reddit = praw.Reddit(
            client_id=os.environ['CLIENT_ID'],
            client_secret=os.environ['CLIENT_SECRET'],
            user_agent=os.environ['USER_AGENT'],
            username=os.environ['USERNAME'],
            password=os.environ['PASSWORD']
        )

    try:
        return list(filter(
                lambda submission: any(keyword in submission.title.lower() for keyword in keywords),
                reddit.subreddit(tracked_subreddits).new(limit=10)
        ))
    except:
        time.sleep(10)
        print('Failed to get scrapped submissions')

        return []