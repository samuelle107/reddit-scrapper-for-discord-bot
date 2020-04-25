import datetime
import logging
import os
import praw
import time
from dotenv import load_dotenv

load_dotenv()
    
def get_scraped_submissions(tracked_subreddits, keywords):
    reddit = praw.Reddit(
            client_id=os.environ['CLIENT_ID'],
            client_secret=os.environ['CLIENT_SECRET'],
            user_agent=os.environ['USER_AGENT'],
            username=os.environ['USERNAME'],
            password=os.environ['PASSWORD']
        )

    forbidden_words = ['[H] Paypal [W]', '[EU-', '[SG]']

    try:
        return list(filter(
                lambda submission: any(keyword.lower() in submission.title.lower() for keyword in keywords) and not any(forbidden_word.lower() in submission.title.lower() for forbidden_word in forbidden_words),
                reddit.subreddit(tracked_subreddits).new(limit=10)
        ))
    except:
        time.sleep(10)
        logging.info(f'{str(datetime.datetime.now())}: Failed to get scrapped submissions')

        return []