import asyncio
import datetime
import discord
import logging
import os
import praw
import psycopg2
from db_helper import insert, remove, query_all, does_exist
from discord.ext import commands
from dotenv import load_dotenv
from subreddit_scrapper import get_scraped_submissions

logging.getLogger().setLevel(logging.INFO)

# Get .env keys
load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = 701619618950807665

# Initialize the bot
client = commands.Bot(command_prefix='!')

# Discord functions
@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    logging.info(f'{str(datetime.datetime.now())}: Bot is ready')

    while True:
        logging.info(f'{str(datetime.datetime.now())}: Checking for new submissions: ')
        # Initialize a connection to the database
        con = psycopg2.connect(DATABASE_URL, sslmode='require')
        # # Get all of the subreddits and parse it into a string
        all_subreddits = '+'.join([d[1] for d in query_all(con, 'subreddit')])
        # Get a list of all keywords
        all_keywords = [d[1] for d in query_all(con, 'keyword')]
        logging.info(f'{str(datetime.datetime.now())}: Subreddits: {all_subreddits}')
        logging.info(f'{str(datetime.datetime.now())}: Keywords: {all_keywords}')
        
        submissions = get_scraped_submissions(all_subreddits, all_keywords)

        logging.info(f'{str(datetime.datetime.now())}: Begin scraping')

        for submission in submissions:
            submission_does_exist = does_exist(con, 'submission', 'id', submission.id)

            if not submission_does_exist:
                logging.info(f'{str(datetime.datetime.now())}: Found new submission: {submission.title[:100]}')
                insert(con, 'submission', ['id', 'title'], [submission.id, submission.title[:100]])
                await channel.send(submission.url)

        logging.info(f'{str(datetime.datetime.now())}: Finished scraping')

        # # Close the connection and sleep for 1 minute
        con.close()
        await asyncio.sleep(60)

@client.command()
async def add_keywords(ctx, *arg):
    logging.info(f'{str(datetime.datetime.now())}: Adding keywords: {arg}')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    for keyword in arg:
        insert(con, 'keyword', ['keyword'], [keyword])
        await ctx.send(f'Sucessfully added {keyword}')
    con.close()

@client.command()
async def add_subreddits(ctx, *arg):
    logging.info(f'{str(datetime.datetime.now())}: Adding subreddits: {arg}')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    for subreddit in arg:
        insert(con, 'subreddit', ['subreddit'], [subreddit])
        await ctx.send(f'Sucessfully added {subreddit}')
    con.close()

@client.command()
async def get_keywords(ctx):
    logging.info(f'{str(datetime.datetime.now())}: Getting keywords')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    result = query_all(con, 'keyword')
    await ctx.send(f'The keywords are: {", ".join([d[1] for d in result])}')
    con.close()

@client.command()
async def get_subreddits(ctx):
    logging.info(f'{str(datetime.datetime.now())}: Getting subreddits')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    result = query_all(con, 'subreddit')
    await ctx.send(f'The subreddits are: {", ".join([d[1] for d in result])}')
    con.close()

@client.command()
async def remove_keyword(ctx, arg):
    logging.info(f'{str(datetime.datetime.now())}: Removing {arg}')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    remove(con, 'keyword', 'keyword', arg)
    await ctx.send(f'Removed: {arg}')
    con.close()

client.run(DISCORD_BOT_TOKEN)
