import os
import praw
import time
from typing import List

class SubredditScraper:
    def __init__(self, tracked_subreddit: str, keywords: List[str]):
        self.tracked_subreddit = tracked_subreddit
        self.keywords = keywords

        # Reddit PRAW
        self.reddit = praw.Reddit(
            client_id=os.environ['CLIENT_ID'],
            client_secret=os.environ['CLIENT_SECRET'],
            user_agent=os.environ['USER_AGENT'],
            username=os.environ['USERNAME'],
            password=os.environ['PASSWORD']
        )
    
    def get_scraped_submissions(self):
        try:
            return list(filter(
                    lambda submission: any(keyword in submission.title.lower() for keyword in self.keywords),
                    self.reddit.subreddit(self.tracked_subreddit).new(limit=10)
            ))
        except:
            time.sleep(10)
            print('Failed to get scrapped submissions')

            return []