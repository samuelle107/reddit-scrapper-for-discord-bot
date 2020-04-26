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

    forbidden_words = ['[H] Paypal', '[EU-', '[SG]', '[CA']

    try:

        return list(filter(
            lambda submission: does_contain_any_words(submission.title, keywords) and not does_contain_any_words(submission.title, forbidden_words),
            reddit.subreddit(tracked_subreddits).new(limit=10)
        ))
    except Exception as e:
        logging.info(f'{str(datetime.datetime.now())}: Failed to get scrapped submissions')
        logging.error(f'{str(datetime.datetime.now())}: {e}')
        time.sleep(10)

        return []

def does_contain_any_words(title, words):
    return any(word.lower() in title.lower() for word in words)