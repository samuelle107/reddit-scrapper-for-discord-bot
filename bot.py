import asyncio
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
    logging.info('Bot is ready')

    while True:
        logging.info('Checking for new submissions')
        # Initialize a connection to the database
        con = psycopg2.connect(DATABASE_URL, sslmode='require')
        # Get all of the subreddits and parse it into a string
        all_subreddits = '+'.join([d[1] for d in query_all(con, 'subreddit')])
        # Get a list of all keywords
        all_keywords = [d[1] for d in query_all(con, 'keyword')]
        logging.info(f'Subreddits: {all_subreddits}')
        logging.info(f'Keywords: {all_keywords}')

        # Get the most recent 10 submissions
        for submission in get_scraped_submissions(all_subreddits, all_keywords):
            submission_does_exist = does_exist(con, 'submission', 'id', submission.id)
            logging.info(f'Checking {submission.title}')

            # If the submission is not yet in the database, insert into the database and alert the channel with the URL
            if not submission_does_exist:
                logging.info(f'Found new qualifying submission: {submission.title}')
                insert(con, 'submission', ['id', 'title'], [submission.id, submission.title])
                await channel.send(submission.url)

        # Close the connection and sleep for 1 minute
        con.close()
        await asyncio.sleep(60)

@client.command()
async def add_keywords(ctx, *arg):
    logging.info(f'Adding keywords: {arg}')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    for keyword in arg:
        insert(con, 'keyword', ['keyword'], [keyword])
        await ctx.send(f'Sucessfully added {keyword}')
    con.close()

@client.command()
async def add_subreddits(ctx, *arg):
    logging.info(f'Adding subreddits: {arg}')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    for subreddit in arg:
        insert(con, 'subreddit', ['subreddit'], [subreddit])
        await ctx.send(f'Sucessfully added {subreddit}')
    con.close()

@client.command()
async def get_keywords(ctx):
    logging.info('Getting keywords')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    result = query_all(con, 'keyword')
    await ctx.send(f'The keywords are: {", ".join([d[1] for d in result])}')
    con.close()

@client.command()
async def get_subreddits(ctx):
    logging.info('Getting subreddits')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    result = query_all(con, 'subreddit')
    await ctx.send(f'The subreddits are: {", ".join([d[1] for d in result])}')
    con.close()

@client.command()
async def remove_keyword(ctx, arg):
    logging.info(f'Removing {arg}')
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    remove(con, 'keyword', 'keyword', arg)
    await ctx.send(f'Removed: {arg}')
    con.close()

client.run(DISCORD_BOT_TOKEN)
