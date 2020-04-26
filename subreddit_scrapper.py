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
        submissions = reddit.subreddit(tracked_subreddits).new(limit=10)
        does_contain_keywords = any(keyword.lower() in submission.title.lower() for keyword in keywords)
        does_contain_forbidden_words = any(forbidden_word.lower() in submission.title.lower() for forbidden_word in forbidden_words)

        return list(filter(lambda submission:  does_contain_keywords and not does_contain_forbidden_words, submissions))
    except:
        logging.info(f'{str(datetime.datetime.now())}: Failed to get scrapped submissions')
        time.sleep(10)

        return []